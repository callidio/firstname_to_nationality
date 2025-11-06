#!/usr/bin/env python
"""
Command-line interface for firstname_to_nationality package.
"""

import sys
import argparse
from firstname_to_nationality import NationalityPredictor


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Predict nationality from first names',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s Michael
  %(prog)s Maria
  %(prog)s --api-key YOUR_KEY John
  %(prog)s --top 3 Pierre
        """
    )
    
    parser.add_argument('name', help='First name to analyze')
    parser.add_argument('--api-key', help='API key for Nationalize.io (optional)')
    parser.add_argument('--top', type=int, default=5, help='Number of top predictions to show (default: 5)')
    
    args = parser.parse_args()
    
    try:
        predictor = NationalityPredictor(api_key=args.api_key)
        results = predictor.predict(args.name)
        
        if not results:
            print(f"No nationality predictions found for '{args.name}'")
            return 0
        
        print(f"\nNationality predictions for '{args.name}':")
        print("-" * 50)
        
        for i, result in enumerate(results[:args.top], 1):
            country = result['country_id']
            probability = result['probability']
            print(f"{i}. {country}: {probability:.2%}")
        
        return 0
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
