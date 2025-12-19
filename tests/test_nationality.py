"""
Unit tests for the FirstnameToNationality class.
"""

import pickle
import tempfile
import unittest
from pathlib import Path

from firstname_to_nationality import FirstnameToNationality


class TestFirstnameToNationalityInitialization(unittest.TestCase):
    """Tests for FirstnameToNationality initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_initialization_without_files(self):
        """Test initialization when model and dictionary don't exist."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )
        self.assertIsNotNone(predictor.model)
        self.assertIsNotNone(predictor.label_encoder)
        self.assertEqual(predictor.nationality_dictionary, {})

    def test_initialization_with_dictionary(self):
        """Test initialization with existing dictionary."""
        # Create a test dictionary
        test_dict = {"john": ["American", "British"], "maria": ["Spanish", "Italian"]}
        with open(self.dict_path, "wb") as f:
            pickle.dump(test_dict, f)

        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )
        self.assertEqual(len(predictor.nationality_dictionary), 2)
        self.assertIn("john", predictor.nationality_dictionary)

    def test_initialization_creates_preprocessor(self):
        """Test that initialization creates a preprocessor."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )
        self.assertIsNotNone(predictor.preprocessor)

    def test_initialization_with_invalid_model_path(self):
        """Test initialization with corrupted model file."""
        # Create a corrupted model file
        with open(self.model_path, "wb") as f:
            pickle.dump(12345, f)  # Invalid data

        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )
        # Should fall back to default model
        self.assertIsNotNone(predictor.model)


class TestFirstnameToNationalityTraining(unittest.TestCase):
    """Tests for FirstnameToNationality training functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_train_simple_model(self):
        """Test training a simple model."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "William", "Giuseppe", "Marco", "Hiroshi", "Takeshi"]
        nationalities = [
            "American",
            "American",
            "Italian",
            "Italian",
            "Japanese",
            "Japanese",
        ]

        # Train without saving
        predictor.train(names, nationalities, save_model=False)

        # Model should be fitted
        self.assertIsNotNone(predictor.model)
        self.assertTrue(hasattr(predictor.model, "predict"))

    def test_train_with_multiple_nationalities(self):
        """Test training with multiple nationalities."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "Giuseppe", "Hiroshi", "Hans", "Pierre"] * 3
        nationalities = ["American", "Italian", "Japanese", "German", "French"] * 3

        predictor.train(names, nationalities, save_model=False)

        self.assertIsNotNone(predictor.model)
        self.assertIsNotNone(predictor.label_encoder)

    def test_train_mismatched_lengths(self):
        """Test that training fails with mismatched input lengths."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "William"]
        nationalities = ["American"]  # Wrong length

        with self.assertRaises(ValueError):
            predictor.train(names, nationalities, save_model=False)

    def test_train_empty_lists(self):
        """Test training with empty lists."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        with self.assertRaises(ValueError):
            predictor.train([], [], save_model=False)

    def test_train_single_nationality(self):
        """Test training with only one nationality (should require at least 2 classes)."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "William", "James"] * 2
        nationalities = ["American"] * 6

        # LogisticRegression requires at least 2 classes
        with self.assertRaises(ValueError):
            predictor.train(names, nationalities, save_model=False)


class TestFirstnameToNationalityPrediction(unittest.TestCase):
    """Tests for FirstnameToNationality prediction functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"

        # Create and train a predictor
        self.predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "William", "James"] * 5 + ["Giuseppe", "Marco", "Luigi"] * 5
        nationalities = ["American"] * 15 + ["Italian"] * 15
        self.predictor.train(names, nationalities, save_model=False)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_predict_single_basic(self):
        """Test basic single prediction."""
        results = self.predictor.predict_single("John", use_dict=False)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)  # (nationality, confidence)

    def test_predict_single_top_n(self):
        """Test prediction with multiple results."""
        results = self.predictor.predict_single("John", top_n=2, use_dict=False)

        self.assertLessEqual(len(results), 2)
        for result in results:
            self.assertIsInstance(result[0], str)  # nationality
            self.assertIsInstance(result[1], float)  # confidence

    def test_predict_single_with_dictionary(self):
        """Test prediction using dictionary lookup."""
        # Create a test dictionary
        test_dict = {"john": ["American", "British"]}
        with open(self.dict_path, "wb") as f:
            pickle.dump(test_dict, f)

        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        results = predictor.predict_single("john", use_dict=True)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "American")
        self.assertEqual(results[0][1], 1.0)  # Dictionary results have confidence 1.0

    def test_predict_single_without_dictionary(self):
        """Test prediction without dictionary lookup."""
        results = self.predictor.predict_single("TestName", use_dict=False)

        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_predict_unknown_name(self):
        """Test prediction of completely unknown name."""
        results = self.predictor.predict_single("XYZ123ABC", use_dict=False)

        self.assertIsInstance(results, list)
        # Should return something, even if low confidence


class TestFirstnameToNationalityBatchPrediction(unittest.TestCase):
    """Tests for FirstnameToNationality batch prediction."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"

        self.predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "Giuseppe"] * 5
        nationalities = ["American", "Italian"] * 5
        self.predictor.train(names, nationalities, save_model=False)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_call_method_single_name(self):
        """Test __call__ method with single name."""
        results = self.predictor("John", use_dict=False)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 1)  # One name
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(len(results[0]), 2)  # (name, predictions)

    def test_call_method_multiple_names(self):
        """Test __call__ method with multiple names."""
        results = self.predictor(["John", "Giuseppe"], use_dict=False)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)  # Two names

    def test_call_method_empty_list(self):
        """Test __call__ method with empty list."""
        results = self.predictor([], use_dict=False)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)


class TestFirstnameToNationalityPersistence(unittest.TestCase):
    """Tests for FirstnameToNationality save/load functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.model_path = Path(self.temp_dir) / "test_model.pt"
        self.dict_path = Path(self.temp_dir) / "test_dict.pkl"

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_save_model(self):
        """Test saving model."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "Giuseppe"] * 3
        nationalities = ["American", "Italian"] * 3
        predictor.train(names, nationalities, save_model=True)

        # Check file exists
        self.assertTrue(self.model_path.exists())

    def test_load_saved_model(self):
        """Test loading a saved model."""
        # Train and save
        predictor1 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        names = ["John", "Giuseppe"] * 3
        nationalities = ["American", "Italian"] * 3
        predictor1.train(names, nationalities, save_model=True)

        # Load in new instance
        predictor2 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        # Should be able to predict
        results = predictor2.predict_single("John", use_dict=False)
        self.assertGreater(len(results), 0)

    def test_save_dictionary(self):
        """Test saving dictionary."""
        predictor = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        test_dict = {"john": ["American"], "maria": ["Spanish"]}
        predictor.save_dictionary(test_dict)

        self.assertTrue(self.dict_path.exists())

    def test_load_saved_dictionary(self):
        """Test loading a saved dictionary."""
        predictor1 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        test_dict = {"john": ["American"], "maria": ["Spanish"]}
        predictor1.save_dictionary(test_dict)

        # Load in new instance
        predictor2 = FirstnameToNationality(
            model_path=str(self.model_path), dictionary_path=str(self.dict_path)
        )

        # Verify dictionary was loaded
        self.assertEqual(len(predictor2.nationality_dictionary), 2)
        self.assertIn("john", predictor2.nationality_dictionary)


if __name__ == "__main__":
    unittest.main()
