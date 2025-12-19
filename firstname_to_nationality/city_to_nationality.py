"""
City to Nationality Predictor for Python 3.13+

This module provides city-based nationality prediction using geocoding services.
When a city is provided, it uses geopy to determine the country. Otherwise,
it falls back to name-based prediction.
"""

import time
import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim

from .firstname_to_country import FirstnameToCountry


@dataclass
class CityPrediction:
    """Data class for city-based prediction results."""

    nationality: str
    confidence: float
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    source: str = "name"  # 'city' or 'name'


class CityToNationality:
    """
    City-to-Nationality predictor using geocoding services.

    This class uses geopy's Nominatim geocoder to determine nationality
    from city names. If no city is provided or geocoding fails, it falls
    back to name-based prediction.
    """

    def __init__(
        self,
        user_agent: str = "firstname_to_nationality",
        timeout: int = 5,
        model_path: str = None,
        dictionary_path: str = None,
    ):
        """
        Initialize the CityToNationality predictor.

        Args:
            user_agent: User agent string for Nominatim geocoder
            timeout: Timeout in seconds for geocoding requests
            model_path: Path to the model checkpoint file (optional)
            dictionary_path: Path to the nationality dictionary file (optional)
        """
        # Initialize geocoder
        self.geocoder = Nominatim(user_agent=user_agent, timeout=timeout)
        self.timeout = timeout

        # Initialize country predictor for name-based predictions
        if model_path and dictionary_path:
            self.country_predictor = FirstnameToCountry(model_path, dictionary_path)
        else:
            self.country_predictor = FirstnameToCountry()

    def _geocode_city(
        self, city: str, max_retries: int = 2
    ) -> Optional[Dict[str, str]]:
        """
        Geocode a city to get country information.

        Args:
            city: City name to geocode
            max_retries: Maximum number of retry attempts on timeout

        Returns:
            Dictionary with country_code and country_name, or None if failed
        """
        for attempt in range(max_retries + 1):
            try:
                # Geocode the city
                location = self.geocoder.geocode(
                    city, addressdetails=True, language="en"
                )

                if location and hasattr(location, "raw"):
                    address = location.raw.get("address", {})

                    # Extract country information
                    country_code = address.get("country_code", "").upper()
                    country_name = address.get("country")

                    if country_code and country_name:
                        return {
                            "country_code": country_code,
                            "country_name": country_name,
                        }

                return None

            except GeocoderTimedOut:
                if attempt < max_retries:
                    # Wait before retrying
                    time.sleep(1)
                    continue
                # Timeout - will return None and fallback to name-based prediction
                return None

            except GeocoderServiceError:
                # Service error - will return None and fallback to name-based prediction
                return None

            except Exception:
                # Unexpected error - will return None and fallback to name-based prediction
                return None

    def _country_code_to_nationality(
        self, country_code: str, country_name: str
    ) -> Optional[str]:
        """
        Map country code to nationality using the country predictor's mapping.

        Args:
            country_code: ISO country code (e.g., 'IT', 'US')
            country_name: Country name

        Returns:
            Nationality string or None if not found
        """
        # Search through the nationality_to_country mapping (reverse lookup)
        country_code_lower = country_code.lower()

        for (
            nationality,
            country_info,
        ) in self.country_predictor.nationality_to_country.items():
            if (
                country_info.get("alpha2", "").lower() == country_code_lower
                or country_info.get("country_name", "").lower() == country_name.lower()
            ):
                # Return the nationality with proper capitalization
                return nationality.capitalize()

        # If not found, warn that the CSV needs to be updated
        warnings.warn(
            f"Country '{country_name}' (code: {country_code}) not found in "
            f"nationality mapping. The country_nationality.csv file needs to be updated.",
            UserWarning,
        )
        return None

    def predict_single(
        self,
        name: str,
        city: Optional[str] = None,
        top_n: int = 1,
        use_dict: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Predict nationality for a single name, optionally using city.

        Args:
            name: Input name
            city: Optional city name for geocoding
            top_n: Number of top predictions to return
            use_dict: Whether to use dictionary lookup first

        Returns:
            List of dictionaries with prediction results
        """
        # If city is provided, try geocoding first
        if city and city.strip():
            city_info = self._geocode_city(city.strip())

            if city_info:
                # Successfully geocoded city
                country_code = city_info["country_code"]
                country_name = city_info["country_name"]
                nationality = self._country_code_to_nationality(
                    country_code, country_name
                )

                if nationality:
                    # City prediction successful - create base result
                    city_result = {
                        "nationality": nationality,
                        "confidence": 1.0,
                        "country_code": country_code,
                        "country_name": country_name,
                        "source": "city",
                    }

                    # If top_n is 1, return only city prediction
                    if top_n == 1:
                        return [city_result]

                    # If top_n > 1, add name-based predictions to fill remaining slots
                    results = [city_result]
                    name_predictions = self.country_predictor.predict_single(
                        name, top_n=top_n - 1, use_dict=use_dict
                    )

                    for pred in name_predictions:
                        results.append(
                            {
                                "nationality": pred["nationality"],
                                "confidence": pred["confidence"],
                                "country_code": pred.get("country_code"),
                                "country_name": pred.get("country_name"),
                                "source": "name",
                            }
                        )

                    return results

        # Fall back to name-based prediction
        country_predictions = self.country_predictor.predict_single(
            name, top_n=top_n, use_dict=use_dict
        )

        # Convert to our format
        results = []
        for pred in country_predictions:
            result = {
                "nationality": pred["nationality"],
                "confidence": pred["confidence"],
                "country_code": pred.get("country_code"),
                "country_name": pred.get("country_name"),
                "source": "name",
            }
            results.append(result)

        return results

    def predict_batch(
        self,
        names: List[str],
        cities: Optional[List[Optional[str]]] = None,
        top_n: int = 1,
        use_dict: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Predict nationalities for multiple names with optional cities.

        Args:
            names: List of names
            cities: Optional list of city names (same length as names)
            top_n: Number of top predictions per name
            use_dict: Whether to use dictionary lookup

        Returns:
            List of dictionaries with name, city, and predictions
        """
        # Ensure cities list matches names list
        if cities is None:
            cities = [None] * len(names)
        elif len(cities) != len(names):
            raise ValueError("Cities list must have the same length as names list")

        results = []

        for name, city in zip(names, cities):
            predictions = self.predict_single(name, city, top_n, use_dict)
            results.append({"name": name, "city": city, "predictions": predictions})

        return results

    def __call__(
        self,
        names: Union[str, List[str]],
        cities: Optional[Union[str, List[Optional[str]]]] = None,
        top_n: int = 1,
        use_dict: bool = True,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Predict nationalities for one or more names with optional cities.

        Args:
            names: Single name string or list of names
            cities: Single city string or list of cities (optional)
            top_n: Number of top predictions per name
            use_dict: Whether to use dictionary lookup

        Returns:
            For single name: List of prediction dictionaries
            For multiple names: List of results with name, city, and predictions
        """
        # Handle single name case
        if isinstance(names, str):
            city = cities if isinstance(cities, str) else None
            return self.predict_single(names, city, top_n, use_dict)

        # Handle multiple names case
        if isinstance(cities, str):
            # Single city for all names
            cities = [cities] * len(names)

        return self.predict_batch(names, cities, top_n, use_dict)


# Alias for convenience
CityToNat = CityToNationality
