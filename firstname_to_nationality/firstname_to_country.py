"""
Firstname to Country Predictor for Python 3.13+

This module extends the FirstnameToNationality predictor to map names to countries
using a nationality-to-country mapping CSV file.
"""

import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .firstname_to_nationality import FirstnameToNationality

# Constants
COUNTRY_NATIONALITY_CSV = (
    os.path.dirname(os.path.abspath(__file__)) + "/country_nationality.csv"
)


@dataclass
class CountryPrediction:
    """Data class for country prediction results."""

    country_code: str
    country_name: str
    nationality: str
    confidence: float


class FirstnameToCountry:
    """
    Firstname-to-Country predictor.

    This class uses the FirstnameToNationality predictor and maps the results
    to countries using a nationality-to-country CSV mapping.
    """

    def __init__(
        self,
        model_path: str = None,
        dictionary_path: str = None,
        country_csv_path: str = COUNTRY_NATIONALITY_CSV,
    ):
        """
        Initialize the FirstnameToCountry predictor.

        Args:
            model_path: Path to the model checkpoint file (optional)
            dictionary_path: Path to the nationality dictionary file (optional)
            country_csv_path: Path to the country-nationality CSV file
        """
        # Initialize the nationality predictor
        if model_path and dictionary_path:
            self.nationality_predictor = FirstnameToNationality(
                model_path, dictionary_path
            )
        else:
            self.nationality_predictor = FirstnameToNationality()

        # Load country-nationality mapping
        self.country_csv_path = Path(country_csv_path)
        self.nationality_to_country: Dict[str, Dict[str, str]] = {}
        self._load_country_mapping()

    def _load_country_mapping(self) -> None:
        """Load the nationality-to-country mapping from CSV file."""
        if not self.country_csv_path.exists():
            print(f"Warning: Country CSV file not found at {self.country_csv_path}")
            return

        try:
            with open(self.country_csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nationality = row["Nationality (Demonym)"].strip()

                    # Skip invalid entries
                    if not nationality or nationality == "(N/A)":
                        continue

                    # Handle multiple nationalities (e.g., "Argentine / Argentinean")
                    nationalities = [n.strip() for n in nationality.split("/")]

                    for nat in nationalities:
                        # Store mapping from nationality to country info
                        self.nationality_to_country[nat.lower()] = {
                            "country_name": row["Country Name"],
                            "alpha2": row["Alpha-2 Code"],
                            "alpha3": row["Alpha-3 Code"],
                        }

            print(
                f"✅ Loaded {len(self.nationality_to_country)} nationality-to-country mappings"
            )

        except Exception as e:
            print(
                f"Warning: Could not load country mapping from {self.country_csv_path}: {e}"
            )
            self.nationality_to_country = {}

    def _map_nationality_to_country(self, nationality: str) -> Optional[Dict[str, str]]:
        """
        Map a nationality to country information.

        Args:
            nationality: The nationality string

        Returns:
            Dictionary with country_name, alpha2, alpha3 or None if not found
        """
        # Try exact match first (case-insensitive)
        nationality_lower = nationality.lower()
        if nationality_lower in self.nationality_to_country:
            return self.nationality_to_country[nationality_lower]

        # Try partial matches
        for nat_key, country_info in self.nationality_to_country.items():
            if nat_key in nationality_lower or nationality_lower in nat_key:
                return country_info

        return None

    def predict_single(
        self, name: str, top_n: int = 1, use_dict: bool = True
    ) -> List[Dict[str, any]]:
        """
        Predict country for a single name.

        Args:
            name: Input name
            top_n: Number of top predictions to return
            use_dict: Whether to use dictionary lookup first

        Returns:
            List of dictionaries with nationality counts and country codes
        """
        # Get nationality predictions
        nationality_predictions = self.nationality_predictor.predict_single(
            name, top_n=top_n, use_dict=use_dict
        )

        results = []

        for nationality, confidence in nationality_predictions:
            # Map nationality to country
            country_info = self._map_nationality_to_country(nationality)

            result = {
                "nationality": nationality,
                "confidence": confidence,
                "count": 1,  # Count is 1 for single prediction
            }

            if country_info:
                result["country_code"] = country_info["alpha2"]
                result["country_name"] = country_info["country_name"]
                result["alpha3"] = country_info["alpha3"]
            else:
                result["country_code"] = None
                result["country_name"] = None
                result["alpha3"] = None

            results.append(result)

        return results

    def predict_batch(
        self,
        names: List[str],
        top_n: int = 1,
        use_dict: bool = True,
        aggregate: bool = True,
    ) -> Dict[str, any]:
        """
        Predict countries for multiple names with aggregation.

        Args:
            names: List of names
            top_n: Number of top predictions per name
            use_dict: Whether to use dictionary lookup
            aggregate: Whether to aggregate results across all names

        Returns:
            If aggregate=True: Dictionary with aggregated nationality counts and country codes
            If aggregate=False: List of individual predictions per name
        """
        all_predictions = []

        for name in names:
            predictions = self.predict_single(name, top_n=top_n, use_dict=use_dict)
            all_predictions.append({"name": name, "predictions": predictions})

        if not aggregate:
            return all_predictions

        # Aggregate results
        nationality_counts: Dict[str, int] = {}
        country_code_mapping: Dict[str, Dict[str, str]] = {}

        for item in all_predictions:
            for pred in item["predictions"]:
                nationality = pred["nationality"]

                # Count nationalities
                if nationality not in nationality_counts:
                    nationality_counts[nationality] = 0
                nationality_counts[nationality] += 1

                # Store country code mapping
                if nationality not in country_code_mapping and pred["country_code"]:
                    country_code_mapping[nationality] = {
                        "country_code": pred["country_code"],
                        "country_name": pred["country_name"],
                        "alpha3": pred["alpha3"],
                    }

        # Build aggregated result
        result = {"total_names": len(names), "nationalities": []}

        # Sort by count (descending)
        sorted_nationalities = sorted(
            nationality_counts.items(), key=lambda x: x[1], reverse=True
        )

        for nationality, count in sorted_nationalities:
            nat_result = {
                "nationality": nationality,
                "count": count,
                "percentage": round(count / len(names) * 100, 2),
            }

            # Add country information if available
            if nationality in country_code_mapping:
                nat_result.update(country_code_mapping[nationality])
            else:
                nat_result["country_code"] = None
                nat_result["country_name"] = None
                nat_result["alpha3"] = None

            result["nationalities"].append(nat_result)

        return result

    def __call__(
        self,
        names: str | List[str],
        top_n: int = 1,
        use_dict: bool = True,
        aggregate: bool = True,
    ) -> Dict[str, any] | List[Dict[str, any]]:
        """
        Predict countries for one or more names.

        Args:
            names: Single name string or list of names
            top_n: Number of top predictions per name
            use_dict: Whether to use dictionary lookup
            aggregate: Whether to aggregate results (only for multiple names)

        Returns:
            Single prediction list for one name, or aggregated/individual results for multiple names
        """
        if isinstance(names, str):
            return self.predict_single(names, top_n, use_dict)
        else:
            return self.predict_batch(names, top_n, use_dict, aggregate)


# Alias for convenience
FirstnameToCtry = FirstnameToCountry
