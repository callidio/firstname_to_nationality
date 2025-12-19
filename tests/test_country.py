"""
Unit tests for the FirstnameToCountry class.
"""

import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from firstname_to_nationality import FirstnameToCountry


class TestFirstnameToCountryInitialization(unittest.TestCase):
    """Tests for FirstnameToCountry initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        # Create a test CSV file
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
            ["Japan", "JP", "JPN", "Japanese"],
            ["Spain", "ES", "ESP", "Spanish"],
            ["Germany", "DE", "DEU", "German"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test initialization of FirstnameToCountry."""
        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        self.assertIsNotNone(predictor.nationality_predictor)
        self.assertGreater(len(predictor.nationality_to_country), 0)

    def test_initialization_creates_nationality_predictor(self):
        """Test that initialization creates a nationality predictor."""
        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        self.assertIsNotNone(predictor.nationality_predictor)

    def test_initialization_with_custom_paths(self):
        """Test initialization with custom model and dictionary paths."""
        model_path = Path(self.temp_dir) / "model.pt"
        dict_path = Path(self.temp_dir) / "dict.pkl"

        predictor = FirstnameToCountry(
            model_path=str(model_path),
            dictionary_path=str(dict_path),
            country_csv_path=str(self.csv_path),
        )

        self.assertIsNotNone(predictor.nationality_predictor)


class TestCountryMappingLoading(unittest.TestCase):
    """Tests for loading country mapping from CSV."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_load_country_mapping(self):
        """Test loading country mapping from CSV."""
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
            ["Japan", "JP", "JPN", "Japanese"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        self.assertIn("american", predictor.nationality_to_country)
        self.assertIn("italian", predictor.nationality_to_country)
        self.assertIn("japanese", predictor.nationality_to_country)

    def test_country_info_structure(self):
        """Test that country info has correct structure."""
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        american_info = predictor.nationality_to_country["american"]
        self.assertEqual(american_info["alpha2"], "US")
        self.assertEqual(american_info["country_name"], "United States")
        self.assertEqual(american_info["alpha3"], "USA")

    def test_multiple_nationalities_per_country(self):
        """Test handling of multiple nationalities per country."""
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["Argentina", "AR", "ARG", "Argentine / Argentinean"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        # Both should map to Argentina
        self.assertIn("argentine", predictor.nationality_to_country)
        self.assertIn("argentinean", predictor.nationality_to_country)

        self.assertEqual(predictor.nationality_to_country["argentine"]["alpha2"], "AR")
        self.assertEqual(
            predictor.nationality_to_country["argentinean"]["alpha2"], "AR"
        )

    def test_skip_invalid_entries(self):
        """Test that invalid entries are skipped."""
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["Antarctica", "AQ", "ATA", "(N/A)"],  # Should be skipped
            ["United States", "US", "USA", "American"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

        self.assertIn("american", predictor.nationality_to_country)
        # N/A should not be in the mapping
        self.assertNotIn("(n/a)", predictor.nationality_to_country)
        self.assertNotIn("n/a", predictor.nationality_to_country)


class TestNationalityToCountryMapping(unittest.TestCase):
    """Tests for nationality to country mapping functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

        self.predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_map_nationality_exact_match(self):
        """Test exact nationality matching."""
        result = self.predictor._map_nationality_to_country("American")

        self.assertIsNotNone(result)
        self.assertEqual(result["alpha2"], "US")
        self.assertEqual(result["country_name"], "United States")

    def test_map_nationality_case_insensitive(self):
        """Test case-insensitive matching."""
        result1 = self.predictor._map_nationality_to_country("american")
        result2 = self.predictor._map_nationality_to_country("AMERICAN")
        result3 = self.predictor._map_nationality_to_country("American")

        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)

    def test_map_unknown_nationality(self):
        """Test mapping of unknown nationality."""
        result = self.predictor._map_nationality_to_country("Martian")

        self.assertIsNone(result)

    def test_map_nationality_partial_match(self):
        """Test partial matching of nationalities."""
        # This tests that partial matches work if implemented
        result = self.predictor._map_nationality_to_country("Italian")

        self.assertIsNotNone(result)
        self.assertEqual(result["alpha2"], "IT")


class TestCountryPredictionSingle(unittest.TestCase):
    """Tests for single name country prediction."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_single_basic(self, mock_nationality_class):
        """Test basic single name prediction."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.return_value = [("American", 0.95)]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_single("John Smith", top_n=1)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["nationality"], "American")
        self.assertEqual(results[0]["country_code"], "US")
        self.assertEqual(results[0]["country_name"], "United States")
        self.assertEqual(results[0]["confidence"], 0.95)
        self.assertEqual(results[0]["count"], 1)

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_single_multiple_results(self, mock_nationality_class):
        """Test single prediction with multiple results."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.return_value = [
            ("American", 0.7),
            ("Italian", 0.3),
        ]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_single("Test Name", top_n=2)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["country_code"], "US")
        self.assertEqual(results[1]["country_code"], "IT")

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_single_unknown_nationality(self, mock_nationality_class):
        """Test prediction with unknown nationality."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.return_value = [("Unknown", 0.5)]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_single("Test Name", top_n=1)

        self.assertEqual(len(results), 1)
        self.assertIsNone(results[0]["country_code"])
        self.assertIsNone(results[0]["country_name"])


class TestCountryPredictionBatch(unittest.TestCase):
    """Tests for batch country prediction."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_batch_aggregated(self, mock_nationality_class):
        """Test batch prediction with aggregation."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.side_effect = [
            [("American", 0.9)],
            [("American", 0.85)],
            [("Italian", 0.95)],
        ]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_batch(
            ["John", "William", "Giuseppe"], aggregate=True
        )

        self.assertEqual(results["total_names"], 3)
        self.assertGreater(len(results["nationalities"]), 0)

        # American should be first (2 occurrences)
        top_nationality = results["nationalities"][0]
        self.assertEqual(top_nationality["nationality"], "American")
        self.assertEqual(top_nationality["count"], 2)
        self.assertAlmostEqual(top_nationality["percentage"], 66.67, places=1)
        self.assertEqual(top_nationality["country_code"], "US")

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_batch_non_aggregated(self, mock_nationality_class):
        """Test batch prediction without aggregation."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.side_effect = [
            [("American", 0.9)],
            [("Italian", 0.95)],
        ]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_batch(["John", "Giuseppe"], aggregate=False)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["name"], "John")
        self.assertEqual(results[1]["name"], "Giuseppe")

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_predict_batch_empty_list(self, mock_nationality_class):
        """Test batch prediction with empty list."""
        mock_predictor = MagicMock()
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor.predict_batch([], aggregate=True)

        self.assertEqual(results["total_names"], 0)


class TestCountryPredictionCallMethod(unittest.TestCase):
    """Tests for __call__ method."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
        ]

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_call_single_name(self, mock_nationality_class):
        """Test __call__ with single name."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.return_value = [("Italian", 0.95)]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor("Giuseppe")

        self.assertIsInstance(results, list)
        self.assertEqual(results[0]["nationality"], "Italian")
        self.assertEqual(results[0]["country_code"], "IT")

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_call_multiple_names_aggregated(self, mock_nationality_class):
        """Test __call__ with multiple names and aggregation."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.side_effect = [
            [("American", 0.9)],
            [("Italian", 0.95)],
        ]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor(["John", "Giuseppe"], aggregate=True)

        self.assertIsInstance(results, dict)
        self.assertEqual(results["total_names"], 2)

    @patch("firstname_to_nationality.firstname_to_country.FirstnameToNationality")
    def test_call_multiple_names_non_aggregated(self, mock_nationality_class):
        """Test __call__ with multiple names without aggregation."""
        mock_predictor = MagicMock()
        mock_predictor.predict_single.side_effect = [
            [("American", 0.9)],
            [("Italian", 0.95)],
        ]
        mock_nationality_class.return_value = mock_predictor

        predictor = FirstnameToCountry(country_csv_path=str(self.csv_path))
        predictor.nationality_predictor = mock_predictor

        results = predictor(["John", "Giuseppe"], aggregate=False)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
