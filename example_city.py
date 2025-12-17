#!/usr/bin/env python3
"""
Example usage of the CityToNationality class.

This demonstrates how to predict nationality from names using optional
city information for improved accuracy via geocoding.
"""

from firstname_to_nationality import CityToNationality


def main():
    """Main example function demonstrating CityToNationality usage."""

    print("🌍 City to Nationality Example")
    print("=" * 70)

    # Initialize the predictor
    print("📦 Initializing CityToNationality predictor...")
    predictor = CityToNationality()

    print("\n" + "=" * 70)
    print("1️⃣  Name-Only Prediction (fallback to name-based)")
    print("=" * 70)

    # Test with name only (no city)
    test_names = [
        "Giuseppe Rossi",
        "John Smith",
        "Hiroshi Tanaka",
    ]

    print("\nPredicting without city information:")
    for name in test_names:
        results = predictor(name, top_n=1)
        if results:
            result = results[0]
            print(
                f"  {name:20} → {result['nationality']:15} "
                f"({result['country_name'] or 'Unknown':20}) "
                f"[{result['confidence']:.3f}] (source: {result['source']})"
            )

    print("\n" + "=" * 70)
    print("2️⃣  Name + City Prediction (city-based with geocoding)")
    print("=" * 70)

    # Test with name and city
    test_cases = [
        ("Maria Garcia", "Barcelona"),
        ("John Smith", "London"),
        ("Pierre Dubois", "Paris"),
        ("Hans Mueller", "Berlin"),
        ("Giovanni Romano", "Rome"),
    ]

    print("\nPredicting with city information:")
    for name, city in test_cases:
        results = predictor(name, cities=city, top_n=1)
        if results:
            result = results[0]
            print(
                f"  {name:20} in {city:15} → {result['nationality']:15} "
                f"({result['country_code'] or 'N/A':3}) "
                f"[{result['confidence']:.3f}] (source: {result['source']})"
            )

    print("\n" + "=" * 70)
    print("3️⃣  Batch Prediction with Mixed Cities")
    print("=" * 70)

    # Batch prediction with some cities provided
    names = [
        "Maria Lopez",
        "John Brown",
        "Luigi Ferrari",
        "Zhang Wei",
        "Ahmed Hassan",
    ]

    cities = [
        "Madrid",  # Spain
        None,  # No city - will use name-based prediction
        "Milan",  # Italy
        "Beijing",  # China
        None,  # No city - will use name-based prediction
    ]

    print("\nBatch prediction results:")
    batch_results = predictor(names, cities=cities, top_n=1)

    for item in batch_results:
        name = item["name"]
        city = item["city"] or "N/A"
        pred = item["predictions"][0] if item["predictions"] else {}

        nationality = pred.get("nationality", "Unknown")
        country_name = pred.get("country_name", "Unknown") or "Unknown"
        country_code = pred.get("country_code", "N/A") or "N/A"
        source = pred.get("source", "unknown")
        confidence = pred.get("confidence", 0.0)

        print(
            f"  {name:15} | City: {city:15} | "
            f"{nationality:15} ({country_name:20}, {country_code:3}) "
            f"[{confidence:.3f}] (source: {source})"
        )

    print("\n" + "=" * 70)
    print("4️⃣  Top-N Predictions")
    print("=" * 70)

    # Get multiple predictions
    print("\nTop 3 predictions for 'Maria' from 'Barcelona':")
    results = predictor("Maria", cities="Barcelona", top_n=3)

    for i, result in enumerate(results, 1):
        nationality = result["nationality"]
        confidence = result["confidence"]
        country = result.get("country_name", "Unknown") or "Unknown"
        code = result.get("country_code", "N/A") or "N/A"
        source = result["source"]

        print(
            f"  {i}. {nationality:15} - {country:20} ({code:3}) "
            f"[{confidence:.3f}] (source: {source})"
        )

    print("\n" + "=" * 70)
    print("5️⃣  Error Handling - Invalid City")
    print("=" * 70)

    # Test with invalid city (should fallback to name-based)
    print("\nTesting with invalid city (should fallback to name):")
    results = predictor("Giuseppe", cities="InvalidCityName12345", top_n=1)

    if results:
        result = results[0]
        print(
            f"  Giuseppe from InvalidCity → {result['nationality']} "
            f"(source: {result['source']}, confidence: {result['confidence']:.3f})"
        )
        if result["source"] == "name":
            print("  ✓ Successfully fell back to name-based prediction")

    print("\n✨ Example completed!")
    print("\n📚 Key features:")
    print("   • City-based nationality prediction using geopy geocoding")
    print("   • Automatic fallback to name-based prediction when:")
    print("     - No city is provided")
    print("     - City geocoding fails or times out")
    print("     - City is invalid or not found")
    print("   • Handles GeocoderTimedOut and GeocoderServiceError exceptions")
    print("   • Returns both nationality and country code")
    print("   • Supports single and batch predictions")
    print("   • Includes prediction source ('city' or 'name') in results")
    print("\n⚠️  Note: Geocoding requires internet connectivity")
    print("   Results may vary based on Nominatim service availability")


if __name__ == "__main__":
    main()
