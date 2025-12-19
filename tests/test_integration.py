"""
Integration tests for the complete workflow.
"""

import csv
import tempfile
import unittest
from pathlib import Path

from firstname_to_nationality import FirstnameToCountry, FirstnameToNationality


class TestEndToEndWorkflow(unittest.TestCase):
    """Integration tests for complete end-to-end workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"
        self.csv_path = Path(self.temp_dir) / "test_countries.csv"

        # Create test CSV
        csv_data = [
            ["Country Name", "Alpha-2 Code", "Alpha-3 Code", "Nationality (Demonym)"],
            ["United States", "US", "USA", "American"],
            ["Italy", "IT", "ITA", "Italian"],
            ["Japan", "JP", "JPN", "Japanese"],
            ["Germany", "DE", "DEU", "German"],
            ["France", "FR", "FRA", "French"],
        ]
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(csv_data)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_nationality_prediction_workflow(self):
        """Test complete nationality prediction workflow."""
        # Create predictor
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        # Train model
        names = ["John", "William", "James"] * 5 + ["Giuseppe", "Marco", "Luigi"] * 5
        nationalities = ["American"] * 15 + ["Italian"] * 15
        predictor.train(names, nationalities, save_model=True)

        # Make predictions
        results = predictor.predict_single("John", use_dict=False)

        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0][0], str)  # nationality
        self.assertIsInstance(results[0][1], float)  # confidence

    def test_country_prediction_workflow(self):
        """Test complete country prediction workflow."""
        # Train nationality predictor
        nat_predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "William", "James"] * 5 + ["Giuseppe", "Marco", "Luigi"] * 5
        nationalities = ["American"] * 15 + ["Italian"] * 15
        nat_predictor.train(names, nationalities, save_model=True)

        # Create country predictor
        country_predictor = FirstnameToCountry(
            model_path=str(self.model_path),
            dictionary_path=str(self.dict_path),
            country_csv_path=str(self.csv_path),
        )

        # Make predictions
        results = country_predictor.predict_single("John", use_dict=False)

        self.assertGreater(len(results), 0)
        self.assertIn("nationality", results[0])
        self.assertIn("country_code", results[0])

    def test_batch_country_prediction_workflow(self):
        """Test batch country prediction with aggregation."""
        # Train nationality predictor
        nat_predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = (
            ["John", "William", "James"] * 3
            + ["Giuseppe", "Marco", "Luigi"] * 3
            + ["Hiroshi", "Takeshi", "Kenji"] * 3
        )
        nationalities = ["American"] * 9 + ["Italian"] * 9 + ["Japanese"] * 9
        nat_predictor.train(names, nationalities, save_model=True)

        # Create country predictor
        country_predictor = FirstnameToCountry(
            model_path=str(self.model_path),
            dictionary_path=str(self.dict_path),
            country_csv_path=str(self.csv_path),
        )

        # Make batch predictions
        test_names = ["John", "Giuseppe", "Hiroshi"]
        results = country_predictor.predict_batch(test_names, aggregate=True)

        self.assertEqual(results["total_names"], 3)
        self.assertGreater(len(results["nationalities"]), 0)

    def test_save_and_reload_workflow(self):
        """Test saving and reloading trained model."""
        # Train and save
        predictor1 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "Giuseppe"] * 5
        nationalities = ["American", "Italian"] * 5
        predictor1.train(names, nationalities, save_model=True)

        # Reload and use
        predictor2 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        results = predictor2.predict_single("John", use_dict=False)

        self.assertGreater(len(results), 0)

    def test_mixed_dictionary_and_model_predictions(self):
        """Test using both dictionary and model predictions."""
        import pickle

        # Create dictionary
        test_dict = {"john": ["American", "British"]}
        with open(self.dict_path, "wb") as f:
            pickle.dump(test_dict, f)

        # Train model with at least 2 classes
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["Giuseppe", "Marco"] * 5 + ["Hans", "Klaus"] * 5
        nationalities = ["Italian"] * 10 + ["German"] * 10
        predictor.train(names, nationalities, save_model=True)

        # Dictionary prediction
        dict_results = predictor.predict_single("john", use_dict=True)
        self.assertEqual(dict_results[0][0], "American")
        self.assertEqual(dict_results[0][1], 1.0)

        # Model prediction
        model_results = predictor.predict_single("Giuseppe", use_dict=False)
        self.assertGreater(len(model_results), 0)


class TestDataConsistency(unittest.TestCase):
    """Tests for data consistency across the pipeline."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"
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

    def test_nationality_to_country_mapping_consistency(self):
        """Test that nationality predictions map consistently to countries."""
        # Train nationality model
        nat_predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John"] * 10 + ["Giuseppe"] * 10
        nationalities = ["American"] * 10 + ["Italian"] * 10
        nat_predictor.train(names, nationalities, save_model=True)

        # Get nationality prediction
        nat_results = nat_predictor.predict_single("John", use_dict=False, top_n=1)
        predicted_nationality = nat_results[0][0]

        # Get country prediction
        country_predictor = FirstnameToCountry(
            model_path=str(self.model_path),
            dictionary_path=str(self.dict_path),
            country_csv_path=str(self.csv_path),
        )

        country_results = country_predictor.predict_single(
            "John", use_dict=False, top_n=1
        )

        # Nationalities should match
        self.assertEqual(
            predicted_nationality.lower(), country_results[0]["nationality"].lower()
        )


if __name__ == "__main__":
    unittest.main()
