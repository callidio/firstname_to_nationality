"""
Unit tests for the CityToNationality class.
"""

import unittest
from unittest.mock import MagicMock, patch

from geopy.exc import GeocoderServiceError, GeocoderTimedOut

from firstname_to_nationality import CityToNationality


class TestCityToNationalityInitialization(unittest.TestCase):
    """Tests for CityToNationality initialization."""

    def test_initialization(self):
        """Test initialization of CityToNationality."""
        predictor = CityToNationality()

        self.assertIsNotNone(predictor.geocoder)
        self.assertIsNotNone(predictor.country_predictor)
        self.assertEqual(predictor.timeout, 5)

    def test_initialization_with_custom_timeout(self):
        """Test initialization with custom timeout."""
        predictor = CityToNationality(timeout=10)
        self.assertEqual(predictor.timeout, 10)

    def test_initialization_with_custom_user_agent(self):
        """Test initialization with custom user agent."""
        custom_agent = "test_agent"
        predictor = CityToNationality(user_agent=custom_agent)
        self.assertIsNotNone(predictor.geocoder)


class TestCityToNationalityGeocodingMocked(unittest.TestCase):
    """Tests for CityToNationality geocoding with mocked geopy."""

    def setUp(self):
        """Set up test fixtures."""
        self.predictor = CityToNationality()

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_success(self, mock_nominatim_class):
        """Test successful city geocoding."""
        # Create a fresh predictor with mocked geocoder
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder

        # Mock location response
        mock_location = MagicMock()
        mock_location.raw = {"address": {"country_code": "it", "country": "Italy"}}
        mock_geocoder.geocode.return_value = mock_location

        predictor = CityToNationality()

        result = predictor._geocode_city("Rome")

        self.assertIsNotNone(result)
        self.assertEqual(result["country_code"], "IT")
        self.assertEqual(result["country_name"], "Italy")

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_not_found(self, mock_nominatim_class):
        """Test geocoding when city is not found."""
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder
        mock_geocoder.geocode.return_value = None

        predictor = CityToNationality()
        result = predictor._geocode_city("InvalidCityXYZ")

        self.assertIsNone(result)

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_timeout(self, mock_nominatim_class):
        """Test geocoding timeout handling."""
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder
        mock_geocoder.geocode.side_effect = GeocoderTimedOut("Timeout")

        predictor = CityToNationality()
        result = predictor._geocode_city("SomeCity", max_retries=0)

        self.assertIsNone(result)

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_service_error(self, mock_nominatim_class):
        """Test geocoding service error handling."""
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder
        mock_geocoder.geocode.side_effect = GeocoderServiceError("Service error")

        predictor = CityToNationality()
        result = predictor._geocode_city("SomeCity")

        self.assertIsNone(result)

    @patch("firstname_to_nationality.city_to_nationality.time.sleep")
    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_timeout_with_retry_success(
        self, mock_nominatim_class, mock_sleep
    ):
        """Test geocoding timeout with successful retry."""
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder

        # First call times out, second call succeeds
        mock_location = MagicMock()
        mock_location.raw = {"address": {"country_code": "fr", "country": "France"}}
        mock_geocoder.geocode.side_effect = [
            GeocoderTimedOut("Timeout"),
            mock_location,
        ]

        predictor = CityToNationality()
        result = predictor._geocode_city("Paris", max_retries=2)

        # Should have retried and succeeded
        self.assertIsNotNone(result)
        self.assertEqual(result["country_code"], "FR")
        self.assertEqual(result["country_name"], "France")
        # Verify sleep was called once (before retry)
        mock_sleep.assert_called_once_with(1)
        # Verify geocode was called twice (initial + retry)
        self.assertEqual(mock_geocoder.geocode.call_count, 2)

    @patch("firstname_to_nationality.city_to_nationality.time.sleep")
    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_geocode_city_timeout_with_retry_exhausted(
        self, mock_nominatim_class, mock_sleep
    ):
        """Test geocoding timeout with all retries exhausted."""
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder

        # All calls time out
        mock_geocoder.geocode.side_effect = GeocoderTimedOut("Timeout")

        predictor = CityToNationality()
        result = predictor._geocode_city("SomeCity", max_retries=2)

        # Should return None after all retries
        self.assertIsNone(result)
        # Verify sleep was called twice (before each retry)
        self.assertEqual(mock_sleep.call_count, 2)
        # Verify geocode was called 3 times (initial + 2 retries)
        self.assertEqual(mock_geocoder.geocode.call_count, 3)


class TestCityToNationalityPrediction(unittest.TestCase):
    """Tests for CityToNationality prediction methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.predictor = CityToNationality()

    def test_predict_single_name_only(self):
        """Test prediction with name only (no city)."""
        results = self.predictor.predict_single("John Smith", top_n=1)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIn("nationality", results[0])
        self.assertIn("confidence", results[0])
        self.assertIn("source", results[0])
        self.assertEqual(results[0]["source"], "name")

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_predict_single_with_city_success(self, mock_nominatim_class):
        """Test prediction with city when geocoding succeeds."""
        # Mock successful geocoding
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder

        mock_location = MagicMock()
        mock_location.raw = {"address": {"country_code": "it", "country": "Italy"}}
        mock_geocoder.geocode.return_value = mock_location

        predictor = CityToNationality()
        results = predictor.predict_single("Mario Rossi", city="Rome", top_n=1)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]["source"], "city")
        self.assertIsNotNone(results[0]["country_code"])

    @patch("firstname_to_nationality.city_to_nationality.Nominatim")
    def test_predict_single_with_city_top_n(self, mock_nominatim_class):
        """Test prediction with city respects top_n parameter."""
        # Mock successful geocoding
        mock_geocoder = MagicMock()
        mock_nominatim_class.return_value = mock_geocoder

        mock_location = MagicMock()
        mock_location.raw = {"address": {"country_code": "it", "country": "Italy"}}
        mock_geocoder.geocode.return_value = mock_location

        predictor = CityToNationality()
        results = predictor.predict_single("Mario Rossi", city="Rome", top_n=3)

        self.assertIsInstance(results, list)
        # Should return up to 3 predictions
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 3)
        # First should be city-based
        self.assertEqual(results[0]["source"], "city")
        # If there are more results, they should be name-based
        if len(results) > 1:
            self.assertEqual(results[1]["source"], "name")

    def test_predict_single_with_invalid_city(self):
        """Test prediction with invalid city (fallback to name)."""
        results = self.predictor.predict_single(
            "John Smith", city="InvalidCityXYZ", top_n=1
        )

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        # Should fallback to name-based prediction
        self.assertEqual(results[0]["source"], "name")

    def test_predict_batch_names_only(self):
        """Test batch prediction with names only."""
        names = ["John Smith", "Maria Garcia", "Luigi Ferrari"]
        results = self.predictor.predict_batch(names, top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(names))

        for result in results:
            self.assertIn("name", result)
            self.assertIn("city", result)
            self.assertIn("predictions", result)
            self.assertGreater(len(result["predictions"]), 0)

    def test_predict_batch_with_cities(self):
        """Test batch prediction with cities."""
        names = ["John Smith", "Maria Garcia"]
        cities = ["London", "Barcelona"]

        results = self.predictor.predict_batch(names, cities=cities, top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(names))

        for i, result in enumerate(results):
            self.assertEqual(result["name"], names[i])
            self.assertEqual(result["city"], cities[i])

    def test_predict_batch_cities_length_mismatch(self):
        """Test batch prediction with mismatched cities length."""
        names = ["John Smith", "Maria Garcia"]
        cities = ["London"]  # Wrong length

        with self.assertRaises(ValueError):
            self.predictor.predict_batch(names, cities=cities)

    def test_call_single_name(self):
        """Test __call__ method with single name."""
        results = self.predictor("John Smith", top_n=1)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_call_single_name_with_city(self):
        """Test __call__ method with single name and city."""
        results = self.predictor("John Smith", cities="London", top_n=1)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_call_multiple_names(self):
        """Test __call__ method with multiple names."""
        names = ["John Smith", "Maria Garcia"]
        results = self.predictor(names, top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(names))

    def test_call_multiple_names_with_cities(self):
        """Test __call__ method with multiple names and cities."""
        names = ["John Smith", "Maria Garcia"]
        cities = ["London", "Barcelona"]
        results = self.predictor(names, cities=cities, top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), len(names))


class TestCityToNationalityCountryMapping(unittest.TestCase):
    """Tests for country code to nationality mapping."""

    def setUp(self):
        """Set up test fixtures."""
        self.predictor = CityToNationality()

    def test_country_code_to_nationality_found(self):
        """Test mapping country code to nationality when found."""
        # Assuming "US" maps to "american" in the nationality_to_country dict
        nationality = self.predictor._country_code_to_nationality("US", "United States")

        self.assertIsNotNone(nationality)
        self.assertIsInstance(nationality, str)

    def test_country_code_to_nationality_special_cases(self):
        """Test special case country to nationality mappings."""
        test_cases = [
            ("US", "United States", "American"),
            ("GB", "United Kingdom", "British"),
            ("NL", "The Netherlands", "Dutch"),
        ]

        for code, country, expected in test_cases:
            result = self.predictor._country_code_to_nationality(code, country)
            # Result should be one of the expected nationalities or derived
            self.assertIsNotNone(result)

    def test_country_code_to_nationality_fallback(self):
        """Test behavior when country is not found in CSV mapping."""
        # Test with a country that is not in the mapping
        with self.assertWarns(UserWarning) as warning_context:
            nationality = self.predictor._country_code_to_nationality(
                "XY", "Testcountry"
            )

        # Should return None when not found
        self.assertIsNone(nationality)
        # Should warn that CSV needs to be updated
        self.assertIn("not found in nationality mapping", str(warning_context.warning))


class TestCityToNationalityEdgeCases(unittest.TestCase):
    """Tests for edge cases and error handling."""

    def setUp(self):
        """Set up test fixtures."""
        self.predictor = CityToNationality()

    def test_empty_name(self):
        """Test prediction with empty name."""
        results = self.predictor.predict_single("", top_n=1)

        self.assertIsInstance(results, list)
        # Should still return results even for empty name

    def test_empty_city(self):
        """Test prediction with empty city string."""
        results = self.predictor.predict_single("John Smith", city="", top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(results[0]["source"], "name")

    def test_whitespace_only_city(self):
        """Test prediction with whitespace-only city."""
        results = self.predictor.predict_single("John Smith", city="   ", top_n=1)

        self.assertIsInstance(results, list)
        self.assertEqual(results[0]["source"], "name")

    def test_top_n_multiple(self):
        """Test prediction with multiple top results."""
        results = self.predictor.predict_single("John Smith", top_n=3)

        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)
        self.assertLessEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
