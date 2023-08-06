import json
import logging
from collections import OrderedDict, namedtuple
from copy import deepcopy
from typing import Iterable, List

from django.core.serializers.json import DjangoJSONEncoder

from eveuniverse import __title__
from eveuniverse.core.esitools import is_esi_online
from eveuniverse.models import EveSolarSystem, EveStargate, EveUniverseBaseModel
from eveuniverse.utils import LoggerAddTag

logger = LoggerAddTag(logging.getLogger(__name__), __title__)


_ModelSpec = namedtuple(
    "ModelSpec", ["model_name", "ids", "include_children", "enabled_sections"]
)


# pylint: disable = invalid-name
def ModelSpec(
    model_name: str,
    ids: List[int],
    include_children: bool = False,
    enabled_sections: Iterable[str] = None,
) -> _ModelSpec:
    """Wrapper for creating ModelSpec objects.

    A ModelSpec class defines what objects are to be loaded as test data

    Args:
        model_name: Name of Eve Universe model
        ids: List of Eve IDs to be loaded
        include_children: Whether to also load children of those objects
    """
    return _ModelSpec(
        model_name=model_name,
        ids=ids,
        include_children=include_children,
        enabled_sections=enabled_sections,
    )


def create_testdata(spec: List[ModelSpec], filepath: str) -> None:
    """Loads eve data from ESI as defined by spec and dumps it to file as JSON

    Args:
        spec: Specification of which Eve objects to load. The specification can contain the same model more than once.
        filepath: absolute path of where to store the resulting JSON file
    """

    # clear database
    for MyModel in EveUniverseBaseModel.all_models():
        if MyModel.__name__ != "EveUnit":
            MyModel.objects.all().delete()

    print()
    # Check if ESI is available
    print("Initializing ESI client ...")
    if not is_esi_online():
        raise RuntimeError("ESI not online")

    # load data per spec
    num = 0
    for model_spec in spec:
        num += 1
        ids = set(model_spec.ids)
        print(
            f"Loading {num}/{len(spec)}: {model_spec.model_name} with "
            f"{len(ids)} objects",
            end="",
        )
        MyModel = EveUniverseBaseModel.get_model_class(model_spec.model_name)
        for id in ids:
            print(".", end="")
            MyModel.objects.get_or_create_esi(
                id=id,
                include_children=model_spec.include_children,
                wait_for_children=True,
                enabled_sections=model_spec.enabled_sections,
            )
        print()

    # dump all data into file
    data = OrderedDict()
    for MyModel in EveUniverseBaseModel.all_models():
        if MyModel.objects.count() > 0 and MyModel.__name__ != "EveUnit":
            logger.info(
                "Collecting %d rows for %s", MyModel.objects.count(), MyModel.__name__
            )
            my_data = list(MyModel.objects.all().values())
            for row in my_data:
                try:
                    del row["last_updated"]
                except KeyError:
                    pass

            data[MyModel.__name__] = my_data

    print(f"Writing testdata to: {filepath}")
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, cls=DjangoJSONEncoder, indent=4, sort_keys=True)


def load_testdata_from_dict(testdata: dict) -> None:
    """creates eve objects in the database from testdata dump given as dict

    Args:
        testdata: The dict containing the testdata as created by `create_testdata()`
    """
    for MyModel in EveUniverseBaseModel.all_models():
        model_name = MyModel.__name__
        if model_name in testdata:
            if MyModel.__name__ == "EveStargate":
                for _ in range(2):
                    for obj in deepcopy(testdata[model_name]):
                        try:
                            EveStargate.objects.get(
                                id=obj["destination_eve_stargate_id"]
                            )
                        except EveStargate.DoesNotExist:
                            del obj["destination_eve_stargate_id"]
                            obj["destination_eve_stargate"] = None

                        try:
                            EveSolarSystem.objects.get(
                                id=obj["destination_eve_solar_system_id"]
                            )
                        except EveSolarSystem.DoesNotExist:
                            del obj["destination_eve_solar_system_id"]
                            obj["destination_eve_solar_system"] = None

                        id = obj["id"]
                        del obj["id"]
                        MyModel.objects.update_or_create(id=id, defaults=obj)
            else:
                entries = [MyModel(**obj) for obj in testdata[model_name]]
                MyModel.objects.bulk_create(entries, batch_size=500)


def load_testdata_from_file(filepath: str) -> None:
    """creates eve objects in the database from testdata dump given as JSON file

    Args:
        filepath: Absolute path to the JSON file containing the testdata created by `create_testdata()`
    """
    with open(filepath, "r", encoding="utf-8") as file:
        testdata = json.load(file)

    load_testdata_from_dict(testdata)
