#!/usr/bin/env python3
"""
Example usage of the FirstnameToNationality implementation.

This demonstrates how to use the FirstnameToNationality class with Python 3.13
and machine learning libraries.
"""

from firstname_to_nationality import FirstnameToNationality


def main():
    """Main example function demonstrating the FirstnameToNationality usage."""

    print("🚀 Firstname to Nationality Python 3.13 Example")
    print("=" * 50)

    # Initialize the predictor
    print("📦 Initializing FirstnameToNationality predictor...")
    predictor = FirstnameToNationality()

    # Example names to test
    test_names = [
        "John Smith",
        "Maria Rodriguez",
        "Zhang Wei",
        "Ahmed Hassan",
        "Anna Kowalski",
        "Hiroshi Tanaka",
        "Giuseppe Rossi",
    ]

    print(f"\n🔍 Testing with {len(test_names)} names:")
    print("-" * 30)

    # Single name prediction
    print("\n1️⃣ Single name prediction:")
    for name in test_names[:3]:
        results = predictor.predict_single(name, top_n=3)
        print(f"   {name:15} → {results}")

    # Batch prediction
    print("\n2️⃣ Batch prediction:")
    batch_results = predictor(test_names, top_n=2)

    for name, predictions in batch_results:
        top_prediction = predictions[0] if predictions else ("unknown", 0.0)
        nationality, confidence = top_prediction
        print(f"   {name:15} → {nationality:10} ({confidence:.2f})")

    # Dictionary-based prediction (if dictionary exists)
    print("\n3️⃣ Testing dictionary lookup:")
    dict_test_name = "John"
    dict_results = predictor.predict_single(dict_test_name, use_dict=True)
    model_results = predictor.predict_single(dict_test_name, use_dict=False)

    print(f"   {dict_test_name} (with dict):    {dict_results}")
    print(f"   {dict_test_name} (model only):   {model_results}")

    # Training example (if you have training data)
    print("\n4️⃣ Training a simple model:")
    try:
        # Example training data (normally you'd have much more)
        training_names = [
            "John",
            "William",
            "James",
            "Robert",
            "Michael",
            "Luigi",
            "Marco",
            "Giuseppe",
            "Antonio",
            "Francesco",
            "Hiroshi",
            "Takashi",
            "Kenji",
            "Satoshi",
            "Yuki",
        ]
        training_nationalities = [
            "American",
            "American",
            "American",
            "American",
            "American",
            "Italian",
            "Italian",
            "Italian",
            "Italian",
            "Italian",
            "Japanese",
            "Japanese",
            "Japanese",
            "Japanese",
            "Japanese",
        ]

        # Train the model
        predictor.train(training_names, training_nationalities, save_model=False)
        print("   ✅ Model trained successfully with sample data!")

        # Test the trained model
        test_result = predictor.predict_single("Marco", use_dict=False)
        print(f"   Test prediction for 'Marco': {test_result}")

    except Exception as e:
        print(f"   ⚠️  Training example failed: {e}")

    print("\n✨ Example completed!")
    print("\n📚 Key features of the implementation:")
    print("   • Python 3.13+ compatible")
    print("   • Uses scikit-learn for ML")
    print("   • Type hints and dataclasses")
    print("   • Reliable file handling")
    print("   • Robust preprocessing and error handling")
    print("   • Batch processing support")
    print("   • Easy model training and saving")


if __name__ == "__main__":
    main()
