"""
Firstname to Nationality Predictor for Python 3.13+

An implementation using machine learning libraries and Python 3.13
features for predicting nationality from names.
"""

import os
import pickle
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

# Constants - file paths for model and dictionary
MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "/best-model.pt"
DICTIONARY_PATH = (
    os.path.dirname(os.path.abspath(__file__)) + "/firstname_nationalities.pkl"
)


@dataclass
class PredictionResult:
    """Data class for prediction results."""

    nationality: str
    confidence: float


class NamePreprocessor:
    """Name preprocessing using Python 3.13 features."""

    def __init__(self):
        self.char_patterns = {"space_marker": "▁", "name_separator": " "}

    def preprocess_name(self, name: str) -> str:
        """
        Preprocess name for model input with character-level tokenization.

        Args:
            name: Input name string

        Returns:
            Preprocessed name string
        """
        # Clean and normalize
        name = name.strip().lower()
        name = re.sub(r"[^\w\s-]", "", name)  # Remove special chars except hyphens

        # Replace spaces with special marker
        name = name.replace(" ", self.char_patterns["space_marker"])

        # Character-level tokenization
        return " ".join(char for char in name if char.strip())

    def restore_name(self, processed_name: str) -> str:
        """
        Restore original name format from processed version.

        Args:
            processed_name: Processed name string

        Returns:
            Restored name string
        """
        name = processed_name.replace(" ", "")
        return name.replace(self.char_patterns["space_marker"], " ")


class FirstnameToNationality:
    """
    Firstname-to-Nationality predictor using scikit-learn.

    This implementation uses Python 3.13 features and ML libraries
    for predicting nationality from first names.
    """

    def __init__(
        self, model_path: str = MODEL_PATH, dictionary_path: str = DICTIONARY_PATH
    ):
        """
        Initialize the FirstnameToNationality predictor.

        Args:
            model_path: Path to the model checkpoint file
            dictionary_path: Path to the nationality dictionary file
        """
        self.model_file_path = Path(model_path)
        self.dictionary_file_path = Path(dictionary_path)
        self.preprocessor = NamePreprocessor()

        # Model components
        self.model: Optional[Pipeline] = None
        self.label_encoder: Optional[LabelEncoder] = None
        self.nationality_dictionary: Dict[str, List[str]] = {}

        # Load model and dictionary if they exist
        self._load_model()
        self._load_dictionary()

    def _load_model(self) -> None:
        """Load the trained model from checkpoint."""
        if self.model_file_path.exists():
            try:
                # Try to load as joblib first (new format)
                model_data = joblib.load(self.model_file_path)
                if isinstance(model_data, dict):
                    self.model = model_data.get("model")
                    self.label_encoder = model_data.get("label_encoder")

                    # Validate that model is actually a pipeline
                    if not hasattr(self.model, "fit") or not hasattr(
                        self.model, "predict_proba"
                    ):
                        print(
                            f"Warning: Loaded model is invalid. Creating default model."
                        )
                        self._create_default_model()
                else:
                    # Fallback for direct model loading
                    if hasattr(model_data, "fit") and hasattr(
                        model_data, "predict_proba"
                    ):
                        self.model = model_data
                        self.label_encoder = LabelEncoder()
                    else:
                        print(
                            f"Warning: Model file contains invalid data. Creating default model."
                        )
                        self._create_default_model()
            except Exception as e:
                print(f"Warning: Could not load model from {self.model_file_path}: {e}")
                self._create_default_model()
        else:
            print(
                f"Model file not found at {self.model_file_path}. Creating default model."
            )
            self._create_default_model()

    def _create_default_model(self) -> None:
        """Create a default model pipeline."""
        self.model = Pipeline(
            [
                (
                    "vectorizer",
                    TfidfVectorizer(
                        analyzer="char",
                        ngram_range=(1, 3),
                        max_features=10000,
                        lowercase=True,
                    ),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        random_state=42,
                        max_iter=1000,
                        # multi_class is deprecated and will default to 'multinomial' in sklearn 1.8
                    ),
                ),
            ]
        )
        self.label_encoder = LabelEncoder()

    def _load_dictionary(self) -> None:
        """Load the name-to-nationality dictionary."""
        if self.dictionary_file_path.exists():
            try:
                with open(self.dictionary_file_path, "rb") as f:
                    self.nationality_dictionary = pickle.load(f)
            except Exception as e:
                print(
                    f"Warning: Could not load dictionary from {self.dictionary_file_path}: {e}"
                )
                self.nationality_dictionary = {}
        else:
            print(f"Dictionary file not found at {self.dictionary_file_path}.")
            self.nationality_dictionary = {}

    def _get_top_predictions(
        self, probabilities: np.ndarray, top_n: int
    ) -> List[PredictionResult]:
        """
        Get top N predictions from model probabilities.

        Args:
            probabilities: Model prediction probabilities
            top_n: Number of top predictions to return

        Returns:
            List of prediction results
        """
        if self.label_encoder is None:
            return [PredictionResult("unknown", 0.0)]

        # Get top indices and their probabilities
        top_indices = np.argsort(probabilities)[-top_n:][::-1]

        results = []
        for idx in top_indices:
            nationality = self.label_encoder.inverse_transform([idx])[0]
            confidence = float(probabilities[idx])
            results.append(PredictionResult(nationality, confidence))

        return results

    def predict_single(
        self, name: str, top_n: int = 1, use_dict: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Predict nationality for a single name.

        Args:
            name: Input name
            top_n: Number of top predictions to return
            use_dict: Whether to use dictionary lookup first

        Returns:
            List of (nationality, confidence) tuples
        """
        # Check dictionary first if requested
        if use_dict and name.lower().strip() in self.nationality_dictionary:
            nationalities = self.nationality_dictionary[name.lower().strip()]
            return [(nat, 1.0) for nat in nationalities[:top_n]]

        # Use model prediction
        if self.model is None:
            return [("unknown", 0.0)]

        processed_name = self.preprocessor.preprocess_name(name)

        try:
            # Get prediction probabilities
            probabilities = self.model.predict_proba([processed_name])[0]
            predictions = self._get_top_predictions(probabilities, top_n)

            return [(pred.nationality, pred.confidence) for pred in predictions]

        except Exception as e:
            print(f"Error predicting for name '{name}': {e}")
            return [("unknown", 0.0)]

    def __call__(
        self,
        names: Union[str, List[str]],
        top_n: int = 1,
        use_dict: bool = True,
        mini_batch_size: int = 128,
    ) -> List[Tuple[str, List[Tuple[str, float]]]]:
        """
        Predict nationalities for one or more names.

        Args:
            names: Single name string or list of names
            top_n: Number of top predictions per name
            use_dict: Whether to use dictionary lookup
            mini_batch_size: Batch size for processing (compatibility parameter)

        Returns:
            List of (name, predictions) tuples where predictions is
            a list of (nationality, confidence) tuples
        """
        # Ensure names is a list
        if isinstance(names, str):
            names = [names]

        results = []

        # Process names (batch processing could be added here for large datasets)
        for name in names:
            predictions = self.predict_single(name, top_n, use_dict)
            results.append((name, predictions))

        return results

    def train(
        self, names: List[str], nationalities: List[str], save_model: bool = True
    ) -> None:
        """
        Train the model on name-nationality pairs.

        Args:
            names: List of names for training
            nationalities: List of corresponding nationalities
            save_model: Whether to save the trained model
        """
        if len(names) != len(nationalities):
            raise ValueError("Names and nationalities lists must have the same length")

        # Preprocess names
        processed_names = [self.preprocessor.preprocess_name(name) for name in names]

        # Encode labels
        encoded_labels = self.label_encoder.fit_transform(nationalities)

        # Train the model
        self.model.fit(processed_names, encoded_labels)

        if save_model:
            self.save_model()

    def save_model(self) -> None:
        """Save the trained model and label encoder."""
        model_data = {"model": self.model, "label_encoder": self.label_encoder}

        # Create directory if it doesn't exist
        self.model_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Save using joblib for better compatibility
        joblib.dump(model_data, self.model_file_path)
        print(f"Model saved to {self.model_file_path}")

    def save_dictionary(self, name_dict: Dict[str, List[str]]) -> None:
        """
        Save a name-to-nationality dictionary.

        Args:
            name_dict: Dictionary mapping names to lists of nationalities
        """
        self.dictionary_file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.dictionary_file_path, "wb") as f:
            pickle.dump(name_dict, f)

        # Update internal dictionary
        self.nationality_dictionary = name_dict
        print(f"Dictionary saved to {self.dictionary_file_path}")


# Alias for convenience
FirstnameToNat = FirstnameToNationality
