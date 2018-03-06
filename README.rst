cinema21-py
=======================

.. image:: https://img.shields.io/pypi/v/cinema21.svg
   :alt: PyPI

.. image:: https://img.shields.io/pypi/status/cinema21.svg
   :alt: PyPI - Status

.. image:: https://img.shields.io/pypi/l/cinema21.svg
   :alt: PyPI - License

.. image:: https://img.shields.io/pypi/pyversions/cinema21.svg
   :alt: PyPI - Python Version

A simple wrapper for Cinema21 private API.

***************
Installation
***************
::

    pip install cinema21

***************
Examples
***************
Initialize

>>> import cinema21
>>> cinema = cinema21.Cinema21()

Fetch available city

>>> cinema.cities()
Cities(cities=[list of City object])

Fetch currently playing movie by city

>>> cinema.playing(10)  # 10 is the id of Jakarta
Movies(movies=[list of Movie object])

***************
References
***************

You can read the source code. The whole code is self explanatory.
