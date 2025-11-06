"""
firstname_to_nationality - Predict the most probable nationality from first names

This package provides functionality to predict a person's nationality based on their first name.
It uses the Nationalize.io API to provide nationality predictions with probability scores.
"""

from .predictor import predict_nationality, NationalityPredictor

__version__ = "0.1.0"
__all__ = ["predict_nationality", "NationalityPredictor"]
