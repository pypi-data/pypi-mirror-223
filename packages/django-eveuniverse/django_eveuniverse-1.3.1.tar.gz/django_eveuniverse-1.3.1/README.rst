==================
django-eveuniverse
==================

Complete set of Eve Online Universe models in Django with on-demand
loading from ESI.

|release| |python| |django| |pipeline| |codecov| |Documentation Status|
|license| |pre-commit| |Code style: black| |chat|

Overview
========

*django-eveuniverse* is a foundation app meant to help speed up the
development of Eve Online apps with Django and ESI. It provides all
classic “static” Eve classes as Django models, including all
relationships, ready to be used in your project. Furthermore, all Eve
models have an on-demand loading mechanism for fetching new objects from
ESI.

Here is an overview of the main features:

*  Complete set of ESI's Eve Universe objects as Django models like
   regions, types or planets.
*  On-demand loading mechanism that allows retrieving Eve universe
   objects ad-hoc from ESI
*  Management commands for preloading often used sets of data like the
   map or ships types
*  Eve models come with additional useful features, e.g. a route finder
   between solar systems or image URLs for types
*  Special model EveEntity for quickly resolving Eve Online IDs to names
*  Optional asynchronous loading of eve models and loading of all
   related children. (e.g. load all types for a specific group)
*  Additional models for selected data from the SDE that is not covered
   by ESI, e.g. type materials

Models
======

Models of Eve Universe with relationships:

.. image:: ../aa-eveuniverse_models.png
   :scale: 15 %
   :alt: models with relationships


.. |release| image:: https://img.shields.io/pypi/v/django-eveuniverse?label=release
   :target: https://pypi.org/project/django-eveuniverse/
.. |python| image:: https://img.shields.io/pypi/pyversions/django-eveuniverse
   :target: https://pypi.org/project/django-eveuniverse/
.. |django| image:: https://img.shields.io/pypi/djversions/django-eveuniverse?label=django
   :target: https://pypi.org/project/django-eveuniverse/
.. |pipeline| image:: https://gitlab.com/ErikKalkoken/django-eveuniverse/badges/master/pipeline.svg
   :target: https://gitlab.com/ErikKalkoken/django-eveuniverse/-/pipelines
.. |codecov| image:: https://codecov.io/gl/ErikKalkoken/django-eveuniverse/branch/master/graph/badge.svg?token=YZF6RVSK0P
   :target: https://codecov.io/gl/ErikKalkoken/django-eveuniverse
.. |Documentation Status| image:: https://readthedocs.org/projects/django-eveuniverse/badge/?version=latest
   :target: https://django-eveuniverse.readthedocs.io/en/latest/?badge=latest
.. |license| image:: https://img.shields.io/badge/license-MIT-green
   :target: https://gitlab.com/ErikKalkoken/django-eveuniverse/-/blob/master/LICENSE
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |chat| image:: https://img.shields.io/discord/790364535294132234
   :target: https://discord.gg/zmh52wnfvM
