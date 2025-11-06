#!/usr/bin/env python3
"""
Example usage of the FirstnameToCountry class.

This demonstrates how to predict countries from first names using the
FirstnameToCountry class, which wraps FirstnameToNationality and maps
nationalities to country codes.
"""

from firstname_to_nationality import FirstnameToCountry


def main():
    """Main example function demonstrating FirstnameToCountry usage."""

    print("🌍 Firstname to Country Example")
    print("=" * 60)

    # Initialize the predictor
    print("📦 Initializing FirstnameToCountry predictor...")
    predictor = FirstnameToCountry()

    print("\n" + "=" * 60)
    print("1️⃣  Single Name Prediction")
    print("=" * 60)

    # Single name predictions
    test_names = [
        "Giuseppe Rossi",
        "William Johnson",
        "Hiroshi Tanaka",
        "Maria Garcia",
        "Hans Mueller",
    ]

    for name in test_names:
        results = predictor.predict_single(name, top_n=3, use_dict=False)
        print(f"\n{name}:")
        for i, result in enumerate(results, 1):
            country = result["country_name"] or "Unknown"
            code = result["country_code"] or "N/A"
            nationality = result["nationality"]
            confidence = result["confidence"]
            print(
                f"  {i}. {country:20} ({code:2}) - {nationality:15} [{confidence:.3f}]"
            )

    print("\n" + "=" * 60)
    print("2️⃣  Batch Prediction with Aggregation")
    print("=" * 60)

    # Batch prediction with aggregation
    team_names = [
        "John Smith",
        "William Brown",
        "Giuseppe Verdi",
        "Marco Polo",
        "Luigi Ferrari",
        "Hans Schmidt",
        "Klaus Weber",
        "Hiroshi Yamamoto",
        "Takeshi Tanaka",
        "Maria Rodriguez",
        "Jose Garcia",
        "Pierre Dubois",
    ]

    print(f"\nAnalyzing {len(team_names)} names...")
    aggregated = predictor.predict_batch(
        team_names, top_n=1, use_dict=False, aggregate=True
    )

    print(f"\n📊 Results for {aggregated['total_names']} names:\n")
    print(f"{'Nationality':<20} {'Country':<25} {'Code':<6} {'Count':<8} {'%':<8}")
    print("-" * 75)

    for nat_info in aggregated["nationalities"]:
        nationality = nat_info["nationality"]
        country = nat_info.get("country_name", "Unknown") or "Unknown"
        code = nat_info.get("country_code", "N/A") or "N/A"
        count = nat_info["count"]
        percentage = nat_info["percentage"]

        print(
            f"{nationality:<20} {country:<25} {code:<6} {count:<8} {percentage:<8.1f}%"
        )

    print("\n" + "=" * 60)
    print("3️⃣  Using the __call__ method")
    print("=" * 60)

    # Single name via __call__
    print("\nSingle name:")
    result = predictor("Giovanni Romano", top_n=1)
    print(f"  Name: Giovanni Romano")
    print(f"  Nationality: {result[0]['nationality']}")
    print(f"  Country: {result[0]['country_name']} ({result[0]['country_code']})")
    print(f"  Confidence: {result[0]['confidence']:.3f}")

    # Multiple names via __call__
    print("\nMultiple names (aggregated):")
    names_list = ["Maria Garcia", "Jose Martinez", "Carmen Lopez"]
    aggregated_result = predictor(names_list, aggregate=True)

    print(f"  Analyzed {aggregated_result['total_names']} names")
    print(f"  Top nationality: {aggregated_result['nationalities'][0]['nationality']}")
    print(f"  Country: {aggregated_result['nationalities'][0]['country_name']}")
    print(f"  Code: {aggregated_result['nationalities'][0]['country_code']}")

    print("\n" + "=" * 60)
    print("4️⃣  Individual Results (Non-Aggregated)")
    print("=" * 60)

    # Get individual results without aggregation
    individual_results = predictor(
        ["Alice Wang", "Bob Chen", "Charlie Li"], aggregate=False
    )

    print("\nIndividual predictions:")
    for item in individual_results:
        name = item["name"]
        pred = item["predictions"][0]
        country = pred["country_name"] or "Unknown"
        code = pred["country_code"] or "N/A"
        print(f"  {name:15} → {country:20} ({code})")

    print("\n✨ Example completed!")
    print("\n📚 Key features:")
    print("   • Maps nationalities to country codes (Alpha-2)")
    print("   • Aggregates results for multiple names")
    print("   • Returns nationality counts and percentages")
    print("   • Supports both individual and batch predictions")
    print("   • Uses country_nationality.csv for mapping")


if __name__ == "__main__":
    main()
