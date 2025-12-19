#!/usr/bin/env python3
"""
Training script for Firstname to Nationality prediction model.

This script provides utilities for training the FirstnameToNationality model with your own data.
"""

import sys
import pickle
from pathlib import Path
from typing import List, Tuple, Dict
import pandas as pd
from firstname_to_nationality import FirstnameToNationality


def load_training_data(file_path: str) -> Tuple[List[str], List[str]]:
    """
    Load training data from a CSV file.

    Expected format: CSV with columns 'name' and 'nationality'

    Args:
        file_path: Path to the CSV file

    Returns:
        Tuple of (names, nationalities) lists
    """
    try:
        df = pd.read_csv(file_path)

        if "name" not in df.columns or "nationality" not in df.columns:
            raise ValueError("CSV must have 'name' and 'nationality' columns")

        names = df["name"].astype(str).tolist()
        nationalities = df["nationality"].astype(str).tolist()

        print(f"✅ Loaded {len(names)} training examples from {file_path}")
        return names, nationalities

    except Exception as e:
        print(f"❌ Error loading training data: {e}")
        sys.exit(1)


def load_dictionary_data(
    dict_path: str, max_samples: int = None
) -> Tuple[List[str], List[str]]:
    """
    Load training data from the firstname_nationalities.pkl dictionary.

    Args:
        dict_path: Path to the pickle dictionary file
        max_samples: Maximum number of samples to load (None for all)

    Returns:
        Tuple of (names, nationalities) lists
    """
    try:
        with open(dict_path, "rb") as f:
            name_dict = pickle.load(f)

        names = []
        nationalities = []

        for name, nat_list in name_dict.items():
            # Use the first nationality for each name
            if nat_list:
                names.append(name)
                nationalities.append(nat_list[0])

            # Stop if we've reached max_samples
            if max_samples and len(names) >= max_samples:
                break

        print(f"✅ Loaded {len(names)} training examples from dictionary")
        return names, nationalities

    except Exception as e:
        print(f"❌ Error loading dictionary data: {e}")
        sys.exit(1)


def create_sample_data() -> Tuple[List[str], List[str]]:
    """
    Create sample training data for demonstration.

    Returns:
        Tuple of (names, nationalities) lists
    """
    sample_data = {
        "American": [
            "John Smith",
            "Michael Johnson",
            "William Brown",
            "James Davis",
            "Robert Miller",
            "David Wilson",
            "Richard Moore",
            "Joseph Taylor",
            "Jennifer Anderson",
            "Lisa Thomas",
            "Nancy Jackson",
            "Karen White",
        ],
        "Italian": [
            "Giuseppe Rossi",
            "Marco Ferrari",
            "Luigi Romano",
            "Antonio Ricci",
            "Francesco Marino",
            "Alessandro Greco",
            "Giovanni Bruno",
            "Andrea Conti",
            "Francesca Bianchi",
            "Giulia Russo",
            "Chiara Colombo",
            "Elena Rizzo",
        ],
        "Japanese": [
            "Hiroshi Tanaka",
            "Takeshi Yamamoto",
            "Kenji Watanabe",
            "Satoshi Ito",
            "Yuki Nakamura",
            "Akira Kobayashi",
            "Masaki Sato",
            "Ryo Suzuki",
            "Yoko Takahashi",
            "Akiko Tanaka",
            "Emi Watanabe",
            "Miki Yamada",
        ],
        "German": [
            "Hans Mueller",
            "Klaus Schmidt",
            "Wolfgang Weber",
            "Helmut Wagner",
            "Gerhard Fischer",
            "Dieter Becker",
            "Gunter Schulz",
            "Manfred Hoffman",
            "Gisela Richter",
            "Ingrid Klein",
            "Petra Neumann",
            "Sabine Schwarz",
        ],
        "Spanish": [
            "Jose Garcia",
            "Manuel Rodriguez",
            "Francisco Martinez",
            "Antonio Lopez",
            "Jesus Sanchez",
            "Miguel Perez",
            "Pedro Gomez",
            "Rafael Martin",
            "Maria Fernandez",
            "Carmen Gonzalez",
            "Ana Jimenez",
            "Isabel Ruiz",
        ],
    }

    names = []
    nationalities = []

    for nationality, name_list in sample_data.items():
        names.extend(name_list)
        nationalities.extend([nationality] * len(name_list))

    return names, nationalities


def train_model(training_file: str = None, use_dictionary: bool = False) -> None:
    """
    Train the FirstnameToNationality model.

    Args:
        training_file: Optional path to CSV training file
        use_dictionary: Whether to use the pickle dictionary for training
    """
    print("🚀 Firstname to Nationality Training Script")
    print("=" * 50)

    # Load training data
    if use_dictionary:
        dict_path = (
            Path(__file__).parent
            / "firstname_to_nationality"
            / "firstname_nationalities.pkl"
        )
        if dict_path.exists():
            print("📚 Loading training data from dictionary...")
            names, nationalities = load_dictionary_data(str(dict_path))
        else:
            print(f"❌ Dictionary not found at {dict_path}")
            sys.exit(1)
    elif training_file and Path(training_file).exists():
        names, nationalities = load_training_data(training_file)
    else:
        print("📝 Using sample training data (no training file provided)")
        names, nationalities = create_sample_data()

    # Initialize the predictor
    print("📦 Initializing FirstnameToNationality predictor...")
    predictor = FirstnameToNationality()

    # Display training statistics
    nationality_counts = {}
    for nat in nationalities:
        nationality_counts[nat] = nationality_counts.get(nat, 0) + 1

    print(f"\n📊 Training data statistics:")
    print(f"   Total samples: {len(names)}")
    print(f"   Unique nationalities: {len(nationality_counts)}")

    # Show top 10 nationalities
    sorted_nats = sorted(nationality_counts.items(), key=lambda x: x[1], reverse=True)
    print(f"\n   Top 10 nationalities:")
    for nat, count in sorted_nats[:10]:
        print(f"   {nat:20}: {count:6} samples")

    # Train the model
    print(f"\n🔥 Training model...")
    try:
        predictor.train(names, nationalities, save_model=True)
        print("✅ Model trained and saved successfully!")

        # Test the trained model
        print(f"\n🧪 Testing trained model:")
        test_names = [
            "Giovanni Romano",
            "William Johnson",
            "Hiroshi Sato",
            "Maria Garcia",
            "Hans Mueller",
        ]

        for test_name in test_names:
            result = predictor.predict_single(test_name, use_dict=False, top_n=3)
            print(f"   {test_name:20} → {result}")

    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print(f"\n✨ Training completed!")
    print(f"📁 Model saved to: {predictor.model_file_path}")


def create_sample_dictionary() -> None:
    """Create a sample name-to-nationality dictionary."""
    print("📚 Creating sample dictionary...")

    sample_dict = {
        "john": ["American", "British"],
        "maria": ["Spanish", "Italian", "Portuguese"],
        "mohammed": ["Arabic", "Turkish"],
        "hiroshi": ["Japanese"],
        "giuseppe": ["Italian"],
        "hans": ["German"],
        "pierre": ["French"],
        "ivan": ["Russian"],
        "chen": ["Chinese"],
        "raj": ["Indian"],
    }

    predictor = FirstnameToNationality()
    predictor.save_dictionary(sample_dict)

    print("✅ Sample dictionary created and saved!")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--dict":
            if len(sys.argv) > 2 and sys.argv[2] == "train":
                # Train using dictionary data
                train_model(use_dictionary=True)
            else:
                # Create sample dictionary
                create_sample_dictionary()
        else:
            train_model(sys.argv[1])
    else:
        print("Usage:")
        print(
            "  python nationality_trainer.py                    # Train with sample data"
        )
        print(
            "  python nationality_trainer.py data.csv           # Train with CSV file"
        )
        print(
            "  python nationality_trainer.py --dict train       # Train with pickle dictionary"
        )
        print(
            "  python nationality_trainer.py --dict             # Create sample dictionary"
        )
        print()
        print(
            "Recommended: Use --dict train to train with 1M+ examples from the dictionary"
        )
        print()

        # Ask user what they want to do
        response = input("Train with dictionary data? (y/n): ").lower()
        if response == "y":
            train_model(use_dictionary=True)
        else:
            train_model()


if __name__ == "__main__":
    main()
