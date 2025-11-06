"""
Example script demonstrating the firstname_to_nationality package.
"""

from firstname_to_nationality import predict_nationality, NationalityPredictor


def main():
    """Main function to demonstrate the package functionality"""
    
    print("=" * 60)
    print("Firstname to Nationality Predictor - Examples")
    print("=" * 60)
    print()
    
    # Example 1: Using the convenience function
    print("Example 1: Using predict_nationality() function")
    print("-" * 60)
    
    names = ["Michael", "Maria", "Ahmed", "Yuki", "Pierre"]
    
    for name in names:
        print(f"\nAnalyzing name: {name}")
        try:
            results = predict_nationality(name)
            if results:
                print(f"  Top predictions:")
                for i, result in enumerate(results[:3], 1):  # Show top 3
                    country = result["country_id"]
                    probability = result["probability"]
                    print(f"    {i}. {country}: {probability:.2%}")
            else:
                print(f"  No predictions available")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Example 2: Using NationalityPredictor class")
    print("-" * 60)
    
    # Example 2: Using the NationalityPredictor class
    predictor = NationalityPredictor()
    
    test_names = ["John", "Li", "Ivan"]
    
    for name in test_names:
        print(f"\nAnalyzing name: {name}")
        try:
            # Get the most probable nationality
            most_probable = predictor.get_most_probable_nationality(name)
            if most_probable:
                country = most_probable["country_id"]
                probability = most_probable["probability"]
                print(f"  Most probable nationality: {country} ({probability:.2%})")
            else:
                print(f"  No predictions available")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
