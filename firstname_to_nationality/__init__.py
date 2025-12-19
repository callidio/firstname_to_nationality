# -*- coding: utf-8 -*-
r"""firstname_to_nationality"""
from __future__ import absolute_import

from .city_to_nationality import CityPrediction, CityToNationality
from .firstname_to_country import CountryPrediction, FirstnameToCountry
from .firstname_to_nationality import (
    FirstnameToNationality,
    NamePreprocessor,
    PredictionResult,
)

__all__ = [
    "FirstnameToNationality",
    "FirstnameToCountry",
    "CityToNationality",
    "NamePreprocessor",
    "PredictionResult",
    "CountryPrediction",
    "CityPrediction",
]
