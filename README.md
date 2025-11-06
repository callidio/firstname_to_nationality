# firstname_to_nationality

Predict the most probable nationality from first names using the Nationalize.io API.

## Installation

```bash
pip install -e .
```

Or install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from firstname_to_nationality import predict_nationality

# Get all nationality predictions for a name
results = predict_nationality("Michael")
print(results)
# [{'country_id': 'US', 'probability': 0.0453}, {'country_id': 'AU', 'probability': 0.0382}, ...]
```

### Using the NationalityPredictor Class

```python
from firstname_to_nationality import NationalityPredictor

# Initialize the predictor
predictor = NationalityPredictor()

# Get all predictions
all_predictions = predictor.predict("Maria")
print(all_predictions)

# Get only the most probable nationality
most_probable = predictor.get_most_probable_nationality("Maria")
print(f"Most probable: {most_probable['country_id']} ({most_probable['probability']:.2%})")
```

### With API Key (for higher rate limits)

```python
from firstname_to_nationality import NationalityPredictor

predictor = NationalityPredictor(api_key="your_api_key_here")
results = predictor.predict("John")
```

## Features

- Predict nationality from first names
- Get probability scores for each predicted nationality
- Support for API keys (for higher rate limits)
- Simple and easy-to-use interface

## API

### `predict_nationality(first_name, api_key=None)`

Convenience function to predict nationality from a first name.

**Parameters:**
- `first_name` (str): The first name to analyze
- `api_key` (str, optional): API key for Nationalize.io

**Returns:**
- List of dictionaries containing country codes and probabilities, sorted by probability in descending order

### `NationalityPredictor`

A class for predicting nationality from first names.

**Methods:**
- `predict(first_name)`: Get all nationality predictions for a name
- `get_most_probable_nationality(first_name)`: Get only the most probable nationality

## Data Source

This package uses the [Nationalize.io API](https://nationalize.io/) to predict nationalities based on first names.

## License

MIT License - see LICENSE file for details.
