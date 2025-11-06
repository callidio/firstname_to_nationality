"""
Core functionality for predicting nationality from first names.
"""

import requests
from typing import List, Dict, Optional


class NationalityPredictor:
    """
    A class to predict nationality from first names using the Nationalize.io API.
    """
    
    API_URL = "https://api.nationalize.io/"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NationalityPredictor.
        
        Args:
            api_key: Optional API key for Nationalize.io (for higher rate limits)
        """
        self.api_key = api_key
    
    def predict(self, first_name: str) -> List[Dict[str, any]]:
        """
        Predict the nationality of a person based on their first name.
        
        Args:
            first_name: The first name to analyze
            
        Returns:
            A list of dictionaries containing country codes and probabilities,
            sorted by probability in descending order.
            
        Example:
            >>> predictor = NationalityPredictor()
            >>> predictor.predict("Michael")
            [{'country_id': 'US', 'probability': 0.0453}, ...]
        """
        if not first_name or not isinstance(first_name, str):
            raise ValueError("First name must be a non-empty string")
        
        params = {"name": first_name.strip()}
        if self.api_key:
            params["apikey"] = self.api_key
        
        try:
            response = requests.get(self.API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            countries = data.get("country", [])
            # Sort by probability in descending order
            return sorted(countries, key=lambda x: x.get("probability", 0), reverse=True)
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching nationality data: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching nationality data: {str(e)}")
    
    def get_most_probable_nationality(self, first_name: str) -> Optional[Dict[str, any]]:
        """
        Get the most probable nationality for a given first name.
        
        Args:
            first_name: The first name to analyze
            
        Returns:
            A dictionary with the most probable country code and probability,
            or None if no prediction is available.
            
        Example:
            >>> predictor = NationalityPredictor()
            >>> predictor.get_most_probable_nationality("Michael")
            {'country_id': 'US', 'probability': 0.0453}
        """
        results = self.predict(first_name)
        return results[0] if results else None


def predict_nationality(first_name: str, api_key: Optional[str] = None) -> List[Dict[str, any]]:
    """
    Convenience function to predict nationality from a first name.
    
    Args:
        first_name: The first name to analyze
        api_key: Optional API key for Nationalize.io
        
    Returns:
        A list of dictionaries containing country codes and probabilities,
        sorted by probability in descending order.
        
    Example:
        >>> predict_nationality("Michael")
        [{'country_id': 'US', 'probability': 0.0453}, ...]
    """
    predictor = NationalityPredictor(api_key=api_key)
    return predictor.predict(first_name)
