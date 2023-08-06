"""Managers and Querysets for Eve universe models."""

# pylint: disable = import-outside-toplevel, missing-class-docstring

import datetime as dt
import logging
from abc import ABC, abstractmethod
from collections import defaultdict, namedtuple
from typing import Any, Dict, Iterable, Optional, Set, Tuple
from urllib.parse import urljoin

import requests
from bravado.exception import HTTPNotFound
from django.core.cache import cache
from django.db import models, transaction
from django.db.utils import IntegrityError
from django.utils.timezone import now

from . import __title__
from .app_settings import EVEUNIVERSE_API_SDE_URL, EVEUNIVERSE_BULK_METHODS_BATCH_SIZE
from .constants import POST_UNIVERSE_NAMES_MAX_ITEMS
from .helpers import EveEntityNameResolver, get_or_create_esi_or_none
from .providers import esi
from .utils import LoggerAddTag, chunks

logger = LoggerAddTag(logging.getLogger(__name__), __title__)

FakeResponse = namedtuple("FakeResponse", ["status_code"])
"""
:meta private:
"""


class EveUniverseBaseModelManager(models.Manager):
    """
    :meta private:
    """

    def _defaults_from_esi_obj(
        self, eve_data_obj: dict, enabled_sections: Optional[Set[str]] = None
    ) -> dict:
        """compiles defaults from an esi data object for update/creating the model"""
        defaults = {}
        for field_name, mapping in self.model._esi_mapping(enabled_sections).items():
            if not mapping.is_pk:
                if not isinstance(mapping.esi_name, tuple):
                    if mapping.esi_name in eve_data_obj:
                        esi_value = eve_data_obj[mapping.esi_name]
                    else:
                        esi_value = None
                else:
                    if (
                        mapping.esi_name[0] in eve_data_obj
                        and mapping.esi_name[1] in eve_data_obj[mapping.esi_name[0]]
                    ):
                        esi_value = eve_data_obj[mapping.esi_name[0]][
                            mapping.esi_name[1]
                        ]
                    else:
                        esi_value = None

                if esi_value is not None:
                    if mapping.is_fk:
                        parent_class = mapping.related_model
                        try:
                            value = parent_class.objects.get(id=esi_value)
                        except parent_class.DoesNotExist:
                            value = None
                            if mapping.create_related:
                                try:
                                    (
                                        value,
                                        _,
                                    ) = parent_class.objects.update_or_create_esi(
                                        id=esi_value,
                                        include_children=False,
                                        wait_for_children=True,
                                    )
                                except AttributeError:
                                    pass

                    else:
                        if mapping.is_charfield and esi_value is None:
                            value = ""
                        else:
                            value = esi_value

                    defaults[field_name] = value

        return defaults


class EveUniverseEntityModelManager(EveUniverseBaseModelManager):
    """Manager for most Eve models."""

    def get_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """gets or creates an eve universe object.

        The object is automatically fetched from ESI if it does not exist (blocking).
        Will always get/create parent objects.

        Args:
            id: Eve Online ID of object
            include_children: if child objects should be updated/created as well
            (only when a new object is created)
            wait_for_children: when true child objects will be updated/created blocking
            (if any), else async (only when a new object is created)
            enabled_sections: Sections to load regardless of current settings,
            e.g. `[EveType.Section.DOGMAS]` will always load dogmas for EveTypes
            task_priority: priority of started tasks

        Returns:
            A tuple consisting of the requested object and a created flag
        """
        id = int(id)
        effective_sections = self.model.determine_effective_sections(enabled_sections)
        try:
            enabled_sections_filter = self._enabled_sections_filter(effective_sections)
            obj = self.filter(**enabled_sections_filter).get(id=id)
            return obj, False
        except self.model.DoesNotExist:
            return self.update_or_create_esi(
                id=id,
                include_children=include_children,
                wait_for_children=wait_for_children,
                enabled_sections=effective_sections,
                task_priority=task_priority,
            )

    def _enabled_sections_filter(self, enabled_sections: Iterable[str]) -> dict:
        return {
            "enabled_sections": getattr(self.model.enabled_sections, section)
            for section in enabled_sections
            if str(section) in self.model.Section.values()
        }

    def update_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """updates or creates an Eve universe object by fetching it from ESI (blocking).
        Will always get/create parent objects

        Args:
            id: Eve Online ID of object
            include_children: if child objects should be updated/created as well (if any)
            wait_for_children: when true child objects will be updated/created blocking
            (if any), else async
            enabled_sections: Sections to load regardless of current settings,
            e.g. `[EveType.Section.DOGMAS]` will always load dogmas for EveTypes
            task_priority: priority of started tasks

        Returns:
            A tuple consisting of the requested object and a created flag
        """
        id = int(id)
        effective_sections = self.model.determine_effective_sections(enabled_sections)
        eve_data_obj = self._transform_esi_response_for_list_endpoints(
            id, self._fetch_from_esi(id=id, enabled_sections=effective_sections)
        )
        if eve_data_obj:
            defaults = self._defaults_from_esi_obj(eve_data_obj, effective_sections)
            obj, created = self.update_or_create(id=id, defaults=defaults)
            if effective_sections and hasattr(obj, "enabled_sections"):
                updated_sections = False
                for section in effective_sections:
                    if str(section) in self.model.Section.values():
                        setattr(obj.enabled_sections, section, True)
                        updated_sections = True
                if updated_sections:
                    obj.save()
            inline_objects = self.model._inline_objects(effective_sections)
            if inline_objects:
                self._update_or_create_inline_objects(
                    parent_eve_data_obj=eve_data_obj,
                    parent_obj=obj,
                    inline_objects=inline_objects,
                    wait_for_children=wait_for_children,
                    enabled_sections=effective_sections,
                    task_priority=task_priority,
                )
            if include_children:
                self._update_or_create_children(
                    parent_eve_data_obj=eve_data_obj,
                    include_children=include_children,
                    wait_for_children=wait_for_children,
                    enabled_sections=effective_sections,
                    task_priority=task_priority,
                )
        else:
            raise HTTPNotFound(
                FakeResponse(status_code=404),  # type: ignore
                message=f"{self.model.__name__} object with id {id} not found",
            )
        return obj, created

    def _fetch_from_esi(
        self, id: Optional[int] = None, enabled_sections: Optional[Iterable[str]] = None
    ) -> dict:
        """make request to ESI and return response data.
        Can handle raw ESI response from both list and normal endpoints.
        """
        if id is not None and not self.model._is_list_only_endpoint():
            args = {self.model._esi_pk(): id}
        else:
            args = {}
        category, method = self.model._esi_path_object()
        esi_data = getattr(
            getattr(esi.client, category),
            method,
        )(**args).results()
        return esi_data

    def _transform_esi_response_for_list_endpoints(self, id: int, esi_data) -> dict:
        """Transforms raw ESI response from list endpoints if this is one
        else just passes the ESI response through
        """
        if not self.model._is_list_only_endpoint():
            return esi_data

        esi_pk = self.model._esi_pk()
        for row in esi_data:
            if esi_pk in row and row[esi_pk] == id:
                return row

        raise HTTPNotFound(
            FakeResponse(status_code=404),  # type: ignore
            message=f"{self.model.__name__} object with id {id} not found",
        )

    def _update_or_create_inline_objects(
        self,
        *,
        parent_eve_data_obj: dict,
        parent_obj,
        inline_objects: dict,
        wait_for_children: bool,
        enabled_sections: Iterable[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """updates_or_creates eve objects that are returned "inline" from ESI
        for the parent eve objects as defined for this parent model (if any)
        """
        from .tasks import (
            update_or_create_inline_object as task_update_or_create_inline_object,
        )

        if not parent_eve_data_obj or not parent_obj:
            raise ValueError(
                f"{self.model.__name__}: Tried to create inline object "
                "from empty parent object"
            )

        for inline_field, model_name in inline_objects.items():
            if (
                inline_field in parent_eve_data_obj
                and parent_eve_data_obj[inline_field]
            ):
                inline_model_class = self.model.get_model_class(model_name)
                esi_mapping = inline_model_class._esi_mapping()
                parent_fk = None
                other_pk = None
                parent_class_2 = None
                for field_name, mapping in esi_mapping.items():
                    if mapping.is_pk:
                        if mapping.is_parent_fk:
                            parent_fk = field_name
                        else:
                            other_pk = (field_name, mapping)
                            parent_class_2 = mapping.related_model

                if not parent_fk or not other_pk:
                    raise ValueError(
                        f"ESI Mapping for {model_name} not valid: "
                        f"{parent_fk}, {other_pk}"
                    )

                parent2_model_name = parent_class_2.__name__ if parent_class_2 else None
                other_pk_info = {
                    "name": other_pk[0],
                    "esi_name": other_pk[1].esi_name,
                    "is_fk": other_pk[1].is_fk,
                }
                for eve_data_obj in parent_eve_data_obj[inline_field]:
                    if wait_for_children:
                        self._update_or_create_inline_object(
                            parent_obj_id=parent_obj.id,
                            parent_fk=parent_fk,
                            eve_data_obj=eve_data_obj,
                            other_pk_info=other_pk_info,
                            parent2_model_name=parent2_model_name,
                            inline_model_name=model_name,
                            enabled_sections=enabled_sections,
                        )
                    else:
                        params: Dict[str, Any] = {
                            "kwargs": {
                                "parent_obj_id": parent_obj.id,
                                "parent_fk": parent_fk,
                                "eve_data_obj": eve_data_obj,
                                "other_pk_info": other_pk_info,
                                "parent2_model_name": parent2_model_name,
                                "inline_model_name": model_name,
                                "parent_model_name": type(parent_obj).__name__,
                                "enabled_sections": list(enabled_sections),
                            }
                        }
                        if task_priority:
                            params["priority"] = task_priority
                        task_update_or_create_inline_object.apply_async(**params)  # type: ignore

    def _update_or_create_inline_object(
        self,
        parent_obj_id: int,
        parent_fk: str,
        eve_data_obj: dict,
        other_pk_info: Dict[str, Any],
        parent2_model_name: Optional[str],
        inline_model_name: str,
        enabled_sections: Iterable[str],
    ):
        """Updates or creates a single inline object.
        Will automatically create additional parent objects as needed
        """
        inline_model_class = self.model.get_model_class(inline_model_name)

        args = {f"{parent_fk}_id": parent_obj_id}
        esi_value = eve_data_obj.get(other_pk_info["esi_name"])
        if other_pk_info["is_fk"]:
            parent_class_2 = self.model.get_model_class(parent2_model_name)
            try:
                value = parent_class_2.objects.get(id=esi_value)
            except parent_class_2.DoesNotExist:
                try:
                    value, _ = parent_class_2.objects.update_or_create_esi(id=esi_value)
                except AttributeError:
                    value = None
        else:
            value = esi_value

        key = other_pk_info["name"]
        args[key] = value  # type: ignore
        args["defaults"] = inline_model_class.objects._defaults_from_esi_obj(
            eve_data_obj,
        )
        inline_model_class.objects.update_or_create(**args)

    def _update_or_create_children(
        self,
        *,
        parent_eve_data_obj: dict,
        include_children: bool,
        wait_for_children: bool,
        enabled_sections: Iterable[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """updates or creates child objects as defined for this parent model (if any)"""
        from .tasks import (
            update_or_create_eve_object as task_update_or_create_eve_object,
        )

        if not parent_eve_data_obj:
            raise ValueError(
                f"{self.model.__name__}: Tried to create children "
                "from empty parent object"
            )

        for key, child_class in self.model._children(enabled_sections).items():
            if key in parent_eve_data_obj and parent_eve_data_obj[key]:
                for obj in parent_eve_data_obj[key]:
                    # TODO: Refactor this hack
                    id = obj["planet_id"] if key == "planets" else obj
                    if wait_for_children:
                        child_model_class = self.model.get_model_class(child_class)
                        child_model_class.objects.update_or_create_esi(
                            id=id,
                            include_children=include_children,
                            wait_for_children=wait_for_children,
                            enabled_sections=enabled_sections,
                            task_priority=task_priority,
                        )

                    else:
                        params: Dict[str, Any] = {
                            "kwargs": {
                                "model_name": child_class,
                                "id": id,
                                "include_children": include_children,
                                "wait_for_children": wait_for_children,
                                "enabled_sections": list(enabled_sections),
                                "task_priority": task_priority,
                            },
                        }
                        if task_priority:
                            params["priority"] = task_priority
                        task_update_or_create_eve_object.apply_async(**params)  # type: ignore

    def update_or_create_all_esi(
        self,
        *,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> None:
        """updates or creates all objects of this class from ESI.

        Loading all objects can take a long time. Use with care!

        Args:
            include_children: if child objects should be updated/created as well (if any)
            wait_for_children: when false all objects will be loaded async, else blocking
            enabled_sections: Sections to load regardless of current settings
        """
        from .tasks import (
            update_or_create_eve_object as task_update_or_create_eve_object,
        )

        effective_sections = self.model.determine_effective_sections(enabled_sections)

        if self.model._is_list_only_endpoint():
            esi_pk = self.model._esi_pk()
            for eve_data_obj in self._fetch_from_esi():
                args = {"id": eve_data_obj[esi_pk]}
                args["defaults"] = self._defaults_from_esi_obj(
                    eve_data_obj=eve_data_obj, enabled_sections=effective_sections
                )
                self.update_or_create(**args)

        else:
            if self.model._has_esi_path_list():
                category, method = self.model._esi_path_list()
                ids = getattr(
                    getattr(esi.client, category),
                    method,
                )().results()
                for id in ids:
                    if wait_for_children:
                        self.update_or_create_esi(
                            id=id,
                            include_children=include_children,
                            wait_for_children=wait_for_children,
                            enabled_sections=effective_sections,
                        )
                    else:
                        params: Dict[str, Any] = {
                            "kwargs": {
                                "model_name": self.model.__name__,
                                "id": id,
                                "include_children": include_children,
                                "wait_for_children": wait_for_children,
                                "enabled_sections": list(effective_sections),
                                "task_priority": task_priority,
                            },
                        }
                        if task_priority:
                            params["priority"] = task_priority
                        task_update_or_create_eve_object.apply_async(**params)  # type: ignore

            else:
                raise TypeError(
                    f"ESI does not provide a list endpoint for {self.model.__name__}"
                )

    def bulk_get_or_create_esi(
        self,
        *,
        ids: Iterable[int],
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> models.QuerySet:
        """Gets or creates objects in bulk.

        Nonexisting objects will be fetched from ESI (blocking).
        Will always get/create parent objects.

        Args:
            ids: List of valid IDs of Eve objects
            include_children: when needed to updated/created if child objects should be updated/created as well (if any)
            wait_for_children: when true child objects will be updated/created blocking (if any), else async
            enabled_sections: Sections to load regardless of current settings

        Returns:
            Queryset with all requested eve objects
        """
        ids = set(map(int, ids))
        effective_sections = self.model.determine_effective_sections(enabled_sections)
        enabled_sections_filter = self._enabled_sections_filter(effective_sections)
        existing_ids = set(
            self.filter(id__in=ids)
            .filter(**enabled_sections_filter)
            .values_list("id", flat=True)
        )
        for id in ids.difference(existing_ids):
            self.update_or_create_esi(
                id=int(id),
                include_children=include_children,
                wait_for_children=wait_for_children,
                enabled_sections=effective_sections,
                task_priority=task_priority,
            )

        return self.filter(id__in=ids)


class EvePlanetManager(EveUniverseEntityModelManager):
    """
    :meta private:
    """

    def _fetch_from_esi(
        self, id: int, enabled_sections: Optional[Iterable[str]] = None
    ) -> dict:
        from .models import EveSolarSystem

        esi_data = super()._fetch_from_esi(id=id)
        # no need to proceed if all children have been disabled
        if not self.model._children(enabled_sections):
            return esi_data

        if "system_id" not in esi_data:
            raise ValueError("system_id not found in moon response - data error")

        system_id = esi_data["system_id"]
        solar_system_data = EveSolarSystem.objects._fetch_from_esi(id=system_id)
        if "planets" not in solar_system_data:
            raise ValueError("planets not found in solar system response - data error")

        for planet in solar_system_data["planets"]:
            if planet["planet_id"] == id:
                if "moons" in planet:
                    esi_data["moons"] = planet["moons"]

                if "asteroid_belts" in planet:
                    esi_data["asteroid_belts"] = planet["asteroid_belts"]

                return esi_data

        raise ValueError(
            f"Failed to find moon {id} in solar system response for {system_id} "
            f"- data error"
        )


class EvePlanetChildrenManager(EveUniverseEntityModelManager):
    """
    :meta private:
    """

    def __init__(self) -> None:
        super().__init__()
        self._my_property_name = None

    def _fetch_from_esi(
        self, id: int, enabled_sections: Optional[Iterable[str]] = None
    ) -> dict:
        from .models import EveSolarSystem

        if not self._my_property_name:
            raise RuntimeWarning("my_property_name not initialized")

        esi_data = super()._fetch_from_esi(id=id)
        if "system_id" not in esi_data:
            raise ValueError("system_id not found in moon response - data error")

        system_id = esi_data["system_id"]
        solar_system_data = EveSolarSystem.objects._fetch_from_esi(id=system_id)
        if "planets" not in solar_system_data:
            raise ValueError("planets not found in solar system response - data error")

        for planet in solar_system_data["planets"]:
            if (
                self._my_property_name in planet
                and planet[self._my_property_name]
                and id in planet[self._my_property_name]
            ):
                esi_data["planet_id"] = planet["planet_id"]
                return esi_data

        raise ValueError(
            f"Failed to find moon {id} in solar system response for {system_id} "
            f"- data error"
        )


class EveAsteroidBeltManager(EvePlanetChildrenManager):
    """
    :meta private:
    """

    def __init__(self) -> None:
        super().__init__()
        self._my_property_name = "asteroid_belts"


class EveMoonManager(EvePlanetChildrenManager):
    """
    :meta private:
    """

    def __init__(self) -> None:
        super().__init__()
        self._my_property_name = "moons"


class EveStargateManager(EveUniverseEntityModelManager):
    """For special handling of relations

    :meta private:
    """

    def update_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """updates or creates an EveStargate object by fetching it from ESI (blocking).
        Will always get/create parent objects

        Args:
            id: Eve Online ID of object
            include_children: (no effect)
            wait_for_children: (no effect)

        Returns:
            A tuple consisting of the requested object and a created flag
        """
        obj, created = super().update_or_create_esi(
            id=int(id),
            include_children=include_children,
            wait_for_children=wait_for_children,
            task_priority=task_priority,
        )
        if obj:
            if obj.destination_eve_stargate is not None:
                obj.destination_eve_stargate.destination_eve_stargate = obj

                if obj.eve_solar_system is not None:
                    obj.destination_eve_stargate.destination_eve_solar_system = (
                        obj.eve_solar_system
                    )
                obj.destination_eve_stargate.save()

        return obj, created


class EveStationManager(EveUniverseEntityModelManager):
    """For special handling of station services

    :meta private:
    """

    def _update_or_create_inline_objects(
        self,
        *,
        parent_eve_data_obj: dict,
        parent_obj,
        inline_objects: dict,
        wait_for_children: bool,
        enabled_sections: Iterable[str],
        task_priority: Optional[int] = None,
    ) -> None:
        """updates_or_creates station service objects for EveStations"""
        from .models import EveStationService

        if "services" in parent_eve_data_obj:
            services = []
            for service_name in parent_eve_data_obj["services"]:
                service, _ = EveStationService.objects.get_or_create(name=service_name)
                services.append(service)

            if services:
                parent_obj.services.add(*services)


class EveTypeManager(EveUniverseEntityModelManager):
    """
    :meta private:
    """

    def update_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        obj, created = super().update_or_create_esi(
            id=id,
            include_children=include_children,
            wait_for_children=wait_for_children,
            enabled_sections=enabled_sections,
            task_priority=task_priority,
        )
        enabled_sections = self.model.determine_effective_sections(enabled_sections)
        if enabled_sections:
            if self.model.Section.TYPE_MATERIALS in enabled_sections:
                from .models import EveTypeMaterial

                EveTypeMaterial.objects.update_or_create_api(eve_type=obj)
            if self.model.Section.INDUSTRY_ACTIVITIES in enabled_sections:
                from .models import (
                    EveIndustryActivityDuration,
                    EveIndustryActivityMaterial,
                    EveIndustryActivityProduct,
                    EveIndustryActivitySkill,
                )

                EveIndustryActivityDuration.objects.update_or_create_api(eve_type=obj)
                EveIndustryActivityProduct.objects.update_or_create_api(eve_type=obj)
                EveIndustryActivitySkill.objects.update_or_create_api(eve_type=obj)
                EveIndustryActivityMaterial.objects.update_or_create_api(eve_type=obj)
        return obj, created


class EveEntityQuerySet(models.QuerySet):
    """Custom queryset for EveEntity."""

    def update_from_esi(self) -> int:
        """Updates all Eve entity objects in this queryset from ESI."""
        from .models import EveEntity

        return EveEntity.objects.update_from_esi_by_id(self.valid_ids())

    def valid_ids(self) -> Set[int]:
        """Determine valid Ids in this Queryset."""
        return set(
            self.exclude(id__in=self.model.ESI_INVALID_IDS).values_list("id", flat=True)
        )


class EveEntityManagerBase(EveUniverseEntityModelManager):
    """Custom manager for EveEntity"""

    MAX_DEPTH = 5

    def get_queryset(self) -> models.QuerySet:
        return EveEntityQuerySet(self.model, using=self._db)

    def get_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """gets or creates an EvEntity object.

        The object is automatically fetched from ESI if it does not exist (blocking)
        or if it has not yet been resolved.

        Args:
            id: Eve Online ID of object

        Returns:
            A tuple consisting of the requested EveEntity object and a created flag
            Returns a None objects if the ID is invalid
        """
        id = int(id)
        try:
            obj = self.exclude(name="").get(id=id)
            created = False
        except self.model.DoesNotExist:
            obj, created = self.update_or_create_esi(
                id=id,
                include_children=include_children,
                wait_for_children=wait_for_children,
            )

        return obj, created

    def update_or_create_esi(
        self,
        *,
        id: int,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> Tuple[Any, bool]:
        """Update or create an EveEntity object by fetching it from ESI (blocking).

        Args:
            id: Eve Online ID of object
            include_children: (no effect)
            wait_for_children: (no effect)

        Returns:
            A tuple consisting of the requested object and a created flag
            When the ID is invalid the returned object will be None

        Exceptions:
            Raises all HTTP codes of ESI endpoint /universe/names except 404
        """
        id = int(id)
        logger.info("%s: Trying to resolve ID to EveEntity with ESI", id)
        if id in self.model.ESI_INVALID_IDS:
            logger.info("%s: ID is not valid", id)
            return None, False
        try:
            result = esi.client.Universe.post_universe_names(ids=[id]).results()
        except HTTPNotFound:
            logger.info("%s: ID is not valid", id)
            return None, False
        item = result[0]
        return self.update_or_create(
            id=item.get("id"),
            defaults={"name": item.get("name"), "category": item.get("category")},
        )

    def bulk_create_esi(self, ids: Iterable[int]) -> int:
        """bulk create and resolve multiple entities from ESI.
        Will also resolve existing entities, that have no name.

        Args:
            ids: List of valid EveEntity IDs

        Returns:
            Count of updated entities
        """
        ids = set(map(int, ids))
        existing_ids = set(self.filter(id__in=ids).values_list("id", flat=True))
        new_ids = ids.difference(existing_ids)

        if not new_ids:
            return 0

        objects = [self.model(id=id) for id in new_ids]
        self.bulk_create(
            objects,
            batch_size=EVEUNIVERSE_BULK_METHODS_BATCH_SIZE,
            ignore_conflicts=True,
        )
        to_update_qs = self.filter(id__in=new_ids) | self.filter(
            id__in=ids.difference(new_ids), name=""
        )
        return to_update_qs.update_from_esi()  # type: ignore

    def update_or_create_all_esi(
        self,
        *,
        include_children: bool = False,
        wait_for_children: bool = True,
        enabled_sections: Optional[Iterable[str]] = None,
        task_priority: Optional[int] = None,
    ) -> None:
        """not implemented - do not use"""
        raise NotImplementedError()

    def bulk_update_new_esi(self) -> int:
        """updates all unresolved EveEntity objects in the database from ESI.

        Returns:
            Count of updated entities.
        """
        return self.filter(name="").update_from_esi()  # type: ignore

    def bulk_update_all_esi(self):
        """Updates all EveEntity objects in the database from ESI.

        Returns:
            Count of updated entities.
        """
        return self.all().update_from_esi()  # type: ignore

    def resolve_name(self, id: int) -> str:
        """Return the name for the given Eve entity ID
        or an empty string if ID is not valid.
        """
        if id is not None:
            obj, _ = self.get_or_create_esi(id=int(id))
            if obj:
                return obj.name
        return ""

    def fetch_by_names_esi(
        self, names: Iterable[str], update: bool = False
    ) -> models.QuerySet:
        """Fetch entities matching given names.
        Will fetch missing entities from ESI if needed or requested.

        Note that names that are not found by ESI are ignored.

        Args:
            names: Names of entities to fetch
            update: When True will always update from ESI

        Returns:
            query with matching entities.
        """
        names = set(names)
        if update:
            names_to_fetch = names
        else:
            existing_names = set(
                self.filter(name__in=names).values_list("name", flat=True)
            )
            names_to_fetch = names - existing_names
        if names_to_fetch:
            esi_result = self._fetch_names_from_esi(names_to_fetch)
            if esi_result:
                self._update_or_create_entities(esi_result)
        return self.filter(name__in=names)

    def _update_or_create_entities(self, esi_result):
        for category_key, entities in esi_result.items():
            try:
                category = self._map_category_key_to_category(category_key)
            except ValueError:
                logger.warning(
                    "Ignoring entities with unknown category %s: %s",
                    category_key,
                    entities,
                )
                continue

            for entity in entities:
                self.update_or_create(
                    id=entity["id"],
                    defaults={"name": entity["name"], "category": category},
                )

    def _fetch_names_from_esi(self, names: Iterable[str]) -> dict:
        logger.info("Trying to fetch EveEntities from ESI by name")
        result = defaultdict(list)
        for chunk_names in chunks(list(names), 500):
            result_chunk = esi.client.Universe.post_universe_ids(
                names=chunk_names
            ).results()
            for category, entities in result_chunk.items():
                if entities:
                    result[category] += entities
        result_compressed = {
            category: entities for category, entities in result.items() if entities
        }
        return result_compressed

    def _map_category_key_to_category(self, category_key: str) -> str:
        """Map category keys from ESI result to categories."""
        my_map = {
            "alliances": self.model.CATEGORY_ALLIANCE,
            "characters": self.model.CATEGORY_CHARACTER,
            "constellations": self.model.CATEGORY_CONSTELLATION,
            "corporations": self.model.CATEGORY_CORPORATION,
            "factions": self.model.CATEGORY_FACTION,
            "inventory_types": self.model.CATEGORY_INVENTORY_TYPE,
            "regions": self.model.CATEGORY_REGION,
            "systems": self.model.CATEGORY_SOLAR_SYSTEM,
            "stations": self.model.CATEGORY_STATION,
        }
        try:
            return my_map[category_key]
        except KeyError:
            raise ValueError(f"Invalid category: {category_key}") from None

    def bulk_resolve_names(self, ids: Iterable[int]) -> EveEntityNameResolver:
        """returns a map of IDs to names in a resolver object for given IDs

        Args:
            ids: List of valid EveEntity IDs

        Returns:
            EveEntityNameResolver object helpful for quick resolving a large amount
            of IDs
        """
        ids = set(map(int, ids))
        self.bulk_create_esi(ids)
        return EveEntityNameResolver(
            {
                row[0]: row[1]
                for row in self.filter(id__in=ids).values_list("id", "name")
            }
        )

    def update_from_esi_by_id(self, ids: Iterable[int]) -> int:
        """Updates all Eve entity objects by id from ESI."""
        if not ids:
            return 0
        ids = list(set((int(id) for id in ids if id not in self.model.ESI_INVALID_IDS)))
        logger.info("Updating %d entities from ESI", len(ids))
        resolved_counter = 0
        for chunk_ids in chunks(ids, POST_UNIVERSE_NAMES_MAX_ITEMS):
            logger.debug("Trying to resolve the following IDs from ESI:\n%s", chunk_ids)
            resolved_counter = self._resolve_entities_from_esi(chunk_ids)
        return resolved_counter

    def _resolve_entities_from_esi(self, ids: list, depth: int = 1):
        resolved_counter = 0
        try:
            items = esi.client.Universe.post_universe_names(ids=ids).results()
        except HTTPNotFound:
            # if API fails to resolve all IDs, we divide and conquer,
            # trying to resolve each half of the ids separately
            if len(ids) > 1 and depth < self.MAX_DEPTH:
                resolved_counter += self._resolve_entities_from_esi(ids[::2], depth + 1)
                resolved_counter += self._resolve_entities_from_esi(
                    ids[1::2], depth + 1
                )
            else:
                logger.warning("Failed to resolve invalid IDs: %s", ids)
        else:
            resolved_counter += len(items)
            for item in items:
                try:
                    self.update_or_create(
                        id=item["id"],
                        defaults={"name": item["name"], "category": item["category"]},
                    )
                except IntegrityError:
                    pass
        return resolved_counter


EveEntityManager = EveEntityManagerBase.from_queryset(EveEntityQuerySet)


class EveMarketPriceManager(models.Manager):
    def update_from_esi(self, minutes_until_stale: Optional[int] = None) -> int:
        """Updates market prices from ESI. Will only create new price objects
        for EveTypes that already exist in the database.

        Args:
            minutes_until_stale: only prices older then given minutes are regarding
            as stale and will be updated. Will use default (60) if not specified.

        Returns:
            Count of updated types
        """
        from .models import EveType

        minutes_until_stale = (
            self.model.DEFAULT_MINUTES_UNTIL_STALE
            if minutes_until_stale is None
            else minutes_until_stale
        )

        logger.info("Fetching market prices from ESI...")
        entries = esi.client.Market.get_markets_prices().results()
        if not entries:
            return 0

        entries_2 = {int(x["type_id"]): x for x in entries if "type_id" in x}
        with transaction.atomic():
            existing_types_ids = set(EveType.objects.values_list("id", flat=True))
            relevant_prices_ids = set(entries_2.keys()).intersection(existing_types_ids)
            deadline = now() - dt.timedelta(minutes=minutes_until_stale)
            current_prices_ids = set(
                self.filter(updated_at__gt=deadline).values_list(
                    "eve_type_id", flat=True
                )
            )
            need_updating_ids = relevant_prices_ids.difference(current_prices_ids)
            if not need_updating_ids:
                logger.info("Market prices are up to date")
                return 0

            logger.info(
                "Updating market prices for %s types...", len(need_updating_ids)
            )
            self.filter(eve_type_id__in=need_updating_ids).delete()
            market_prices = [
                self.model(
                    eve_type=get_or_create_esi_or_none("type_id", entry, EveType),
                    adjusted_price=entry.get("adjusted_price"),
                    average_price=entry.get("average_price"),
                )
                for type_id, entry in entries_2.items()
                if type_id in need_updating_ids
            ]
            self.bulk_create(
                market_prices, batch_size=EVEUNIVERSE_BULK_METHODS_BATCH_SIZE
            )
            logger.info(
                "Completed updating market prices for %s types.", len(need_updating_ids)
            )
            return len(market_prices)


class ApiCacheManager(ABC):
    @property
    @abstractmethod
    def sde_cache_key(self) -> str:
        pass

    @property
    @abstractmethod
    def sde_api_route(self) -> str:
        pass

    @property
    def sde_cache_timeout(self):
        return 3600 * 24

    @classmethod
    def _response_to_cache(cls, response: requests.Response) -> dict:
        data_all = {}
        for row in response.json():
            type_id = row["typeID"]
            if type_id not in data_all:
                data_all[type_id] = []
            data_all[type_id].append(row)
        cache.set(
            key=cls.sde_cache_key,
            value=data_all,
            timeout=cls.sde_cache_timeout,
        )
        return data_all

    @classmethod
    def _fetch_sde_data_cached(cls) -> dict:
        data = cache.get(cls.sde_cache_key)
        if not data:
            response = requests.get(
                urljoin(EVEUNIVERSE_API_SDE_URL, "latest/" + cls.sde_api_route),
                timeout=10,
            )
            response.raise_for_status()
            data = cls._response_to_cache(response)
            cache.set(
                key=cls.sde_cache_key,
                value=data,
                timeout=cls.sde_cache_timeout,
            )
        return data

    @classmethod
    @abstractmethod
    def update_or_create_api(cls, *args, **kwargs) -> None:
        pass


class EveTypeMaterialManager(models.Manager, ApiCacheManager):
    sde_cache_key = "EVEUNIVERSE_TYPE_MATERIALS_REQUEST"
    sde_cache_timeout = 3600 * 24
    sde_api_route = "invTypeMaterials.json"

    def update_or_create_api(self, *, eve_type) -> None:
        """updates or creates type material objects for the given eve type"""
        from .models import EveType

        type_material_data_all = self._fetch_sde_data_cached()
        for type_material_data in type_material_data_all.get(eve_type.id, []):
            material_eve_type, _ = EveType.objects.get_or_create_esi(
                id=type_material_data.get("materialTypeID")
            )
            self.update_or_create(
                eve_type=eve_type,
                material_eve_type=material_eve_type,
                defaults={
                    "quantity": type_material_data.get("quantity"),
                },
            )


class EveIndustryActivityDurationManager(models.Manager, ApiCacheManager):
    sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_DURATIONS_REQUEST"
    sde_cache_timeout = 3600 * 24
    sde_api_route = "industryActivity.json"  # not related to EveIndustryActivity

    def update_or_create_api(self, *, eve_type) -> None:
        from eveuniverse.models import EveIndustryActivity

        industry_activity_data_all = self._fetch_sde_data_cached()
        for industry_activity_data in industry_activity_data_all.get(eve_type.id, []):
            activity = EveIndustryActivity.objects.get(
                pk=industry_activity_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                activity=activity,
                defaults={
                    "time": industry_activity_data.get("time"),
                },
            )


class EveIndustryActivityMaterialManager(models.Manager, ApiCacheManager):
    sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_MATERIALS_REQUEST"
    sde_cache_timeout = 3600 * 24
    sde_api_route = "industryActivityMaterials.json"

    def update_or_create_api(self, *, eve_type) -> None:
        """updates or creates industry material objects for the given industry activity"""
        from .models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_material_data in activity_data:
            material_eve_type, _ = EveType.objects.get_or_create_esi(
                id=industry_material_data.get("materialTypeID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_material_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                material_eve_type=material_eve_type,
                activity=activity,
                defaults={
                    "quantity": industry_material_data.get("quantity"),
                },
            )


class EveIndustryActivityProductManager(models.Manager, ApiCacheManager):
    sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_PRODUCTS_REQUEST"
    sde_cache_timeout = 3600 * 24
    sde_api_route = "industryActivityProducts.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from .models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_products_data in activity_data:
            product_eve_type, _ = EveType.objects.get_or_create_esi(
                id=industry_products_data.get("productTypeID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_products_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                product_eve_type=product_eve_type,
                activity=activity,
                defaults={
                    "quantity": industry_products_data.get("quantity"),
                },
            )


class EveIndustryActivitySkillManager(models.Manager, ApiCacheManager):
    sde_cache_key = "EVEUNIVERSE_INDUSTRY_ACTIVITY_SKILLS_REQUEST"
    sde_cache_timeout = 3600 * 24
    sde_api_route = "industryActivitySkills.json"

    def update_or_create_api(self, *, eve_type) -> None:
        from .models import EveIndustryActivity, EveType

        data_all = self._fetch_sde_data_cached()
        activity_data = data_all.get(eve_type.id, {})
        for industry_skill_data in activity_data:
            skill_eve_type, _ = EveType.objects.get_or_create_esi(
                id=industry_skill_data.get("skillID")
            )
            activity = EveIndustryActivity.objects.get(
                pk=industry_skill_data.get("activityID")
            )
            self.update_or_create(
                eve_type=eve_type,
                skill_eve_type=skill_eve_type,
                activity=activity,
                defaults={
                    "level": industry_skill_data.get("level"),
                },
            )
