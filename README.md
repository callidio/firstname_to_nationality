# Firstname to Nationality - Python 3.13 Implementation

A name-to-nationality prediction library for Python 3.13+ using machine learning libraries.

## 🚀 Features

This library provides the following capabilities:

- ✅ **Python 3.13+ Compatible**: Uses Python features and type hints
- ✅ **ML Stack**: Built with scikit-learn for performance and compatibility
- ✅ **City-Based Prediction**: Use geopy geocoding for city-based nationality prediction
- ✅ **Type Safety**: Full type hints and dataclasses throughout
- ✅ **Error Handling**: Robust error handling and fallbacks
- ✅ **Dev Container Ready**: Includes VS Code dev container configuration
- ✅ **Flexible Training**: Easy model training with your own data
- ✅ **Batch Processing**: Efficient batch prediction support

## 📦 Installation

### Using the Dev Container (Recommended)

1. Open in VS Code
2. When prompted, click "Reopen in Container"
3. The dev container will build automatically with Python 3.13

### Manual Installation

```bash
# Ensure you have Python 3.13+
python --version

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## 🔧 Quick Start

### Basic Name-Based Prediction

```python
from firstname_to_nationality import FirstnameToNationality

# Initialize the predictor
predictor = FirstnameToNationality()

# Predict nationality for a single name
result = predictor.predict_single("Giuseppe Rossi", top_n=3)
print(result)  # [('Italian', 0.85), ('Spanish', 0.12), ...]

# Batch prediction
names = ["John Smith", "Maria Rodriguez", "Zhang Wei"]
results = predictor(names, top_n=2)

for name, predictions in results:
    nationality, confidence = predictions[0]
    print(f"{name} → {nationality} ({confidence:.2f})")
```

### City-Based Prediction (New!)

```python
from firstname_to_nationality import CityToNationality

# Initialize the city-based predictor
predictor = CityToNationality()

# Predict with city information (more accurate)
result = predictor("Maria Garcia", cities="Barcelona")
print(result)  # Spanish (from Barcelona, Spain)

# Fallback to name-based prediction if no city
result = predictor("Maria Garcia")
print(result)  # Uses ML model on name

# Batch prediction with cities
names = ["John Smith", "Luigi Ferrari", "Zhang Wei"]
cities = ["London", "Milan", "Beijing"]
results = predictor(names, cities=cities)

for item in results:
    name = item["name"]
    pred = item["predictions"][0]
    print(f"{name} from {item['city']} → {pred['nationality']} ({pred['country_code']})")
```

## 🧪 Examples

Run the example scripts:

```bash
# Basic name-based prediction
python example.py

# Country code mapping
python example_country.py

# City-based prediction with geocoding
python example_city.py
```

## 🔥 Training Your Own Model

### Using Sample Data

```bash
python nationality_trainer.py
```

### Using Your Own Data

Create a CSV file with `name` and `nationality` columns:

```csv
name,nationality
John Smith,American
Giuseppe Rossi,Italian
Hiroshi Tanaka,Japanese
```

Then train:

```bash
python nationality_trainer.py your_data.csv
```

### Creating a Dictionary

```bash
python nationality_trainer.py --dict
```

## 🏗️ Architecture

The implementation consists of:

- **`FirstnameToNationality`**: Main predictor class with scikit-learn backend  
- **`FirstnameToCountry`**: Maps nationalities to country codes
- **`CityToNationality`**: City-based prediction with geocoding fallback to name-based
- **`NamePreprocessor`**: Advanced name preprocessing and normalization
- **`PredictionResult`**: Type-safe prediction results using dataclasses
- **Model Pipeline**: TF-IDF vectorization + Logistic Regression

## 📁 File Structure

The implementation uses these file paths:

- `firstname_to_nationality/best-model.pt`: Model checkpoint file
- `firstname_to_nationality/firstname_nationalities.pkl`: Name-to-nationality dictionary

## � Usage Examples

### Basic Usage
```python
from firstname_to_nationality import FirstnameToNationality
predictor = FirstnameToNationality()
results = predictor(["John Smith"])
```

### Advanced Features
```python
# Type-safe single predictions
result = predictor.predict_single("John Smith", top_n=3)

# Training interface
predictor.train(names, nationalities, save_model=True)

# Dictionary management
predictor.save_dictionary(name_dict)
```

## 🐳 Development with Docker

### Dev Container
The repository includes a complete dev container setup for VS Code:

```bash
# Open in VS Code
code .
# Click "Reopen in Container" when prompted
```

### Manual Docker
```bash
# Build
docker build -f .devcontainer/Dockerfile -t firstname-to-nationality .

# Run
docker run -it --rm -v $(pwd):/workspace firstname-to-nationality
```

## ⚡ Performance

The implementation offers:

- Fast training with scikit-learn
- Memory efficiency
- Batch processing support
- Python optimizations

## 🧬 Dependencies

**Core Requirements:**
- Python 3.13+
- scikit-learn >= 1.3.0
- numpy >= 1.25.0
- pandas >= 2.0.0
- joblib >= 1.3.0
- geopy >= 2.3.0 (for city-based predictions)

**Development:**
- pytest, black, isort, pylint, mypy

## 🤝 Contributing

1. Use the dev container for consistent environment
2. Follow type hints throughout
3. Run tests: `pytest`
4. Format code: `black . && isort .`
5. Check types: `mypy firstname_to_nationality/`

### Setting Up GitHub Actions Workflows

If you're a maintainer and need to set up the auto-version-bump workflow, see [.github/WORKFLOW_SETUP.md](.github/WORKFLOW_SETUP.md) for detailed instructions on configuring the required Personal Access Token or GitHub App.

## 📄 License

MIT License

## � Implementation Details

This is a complete implementation with:

- ✅ Consistent method signatures
- ✅ Reliable file handling
- ✅ Robust prediction results
- ✅ Efficient model format
- ✅ Minimal dependencies

## 🎯 Roadmap

- [ ] Transformer-based models support
- [ ] REST API server
- [ ] Web interface
- [ ] Multi-language support
- [ ] Advanced evaluation metrics