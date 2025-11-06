# Architecture Instructions

## 📋 Project Overview

The **Firstname to Nationality** project is a Python 3.13+ machine learning library that predicts nationality from first names using scikit-learn and modern Python features.

## 🏗️ System Architecture

### Core Components

```
firstname_to_nationality/
├── firstname_to_nationality.py    # Main prediction module
├── best-model.pt                  # Trained model checkpoint
├── firstname_nationalities.pkl   # Name-to-nationality dictionary
└── __init__.py                   # Package initialization
```

### Key Classes

#### 1. `FirstnameToNationality` (Main Class)
- **Purpose**: Primary interface for nationality prediction
- **Dependencies**: scikit-learn, numpy, pandas, joblib
- **Key Methods**:
  - `__init__()`: Initialize with model and dictionary paths
  - `predict_single()`: Predict nationality for one name
  - `__call__()`: Batch prediction interface
  - `train()`: Train model with custom data
  - `save_model()` / `save_dictionary()`: Persistence methods

#### 2. `NamePreprocessor`
- **Purpose**: Handle name preprocessing and normalization
- **Features**:
  - Character-level tokenization
  - Special character handling
  - Space marker replacement (`▁`)
  - Name restoration capabilities

#### 3. `PredictionResult` (Dataclass)
- **Purpose**: Type-safe prediction results
- **Fields**: `nationality: str`, `confidence: float`

### Constants and Paths

```python
# File path constants (maintained for compatibility)
MODEL_PATH = "/path/to/best-model.pt"           # ML model checkpoint
DICTIONARY_PATH = "/path/to/firstname_nationalities.pkl"  # Lookup dictionary
```

## 🔄 Data Flow

### 1. Initialization Flow
```
User creates FirstnameToNationality() 
    ↓
Load model from MODEL_PATH (if exists)
    ↓
Load dictionary from DICTIONARY_PATH (if exists)
    ↓
Initialize NamePreprocessor
    ↓
Ready for predictions
```

### 2. Prediction Flow
```
Input: "Giuseppe Rossi"
    ↓
Check dictionary lookup (if use_dict=True)
    ↓ (if not found)
NamePreprocessor.preprocess_name()
    ↓
"g i u s e p p e ▁ r o s s i"
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression Prediction
    ↓
Top-N Results: [("Italian", 0.85), ("Spanish", 0.12)]
```

### 3. Training Flow
```
Training Data: names[] + nationalities[]
    ↓
Preprocess all names
    ↓
Encode nationality labels
    ↓
Fit TF-IDF + LogisticRegression pipeline
    ↓
Save model to MODEL_PATH
```

## 🧠 Machine Learning Pipeline

### Model Architecture
```python
Pipeline([
    ('vectorizer', TfidfVectorizer(
        analyzer='char',           # Character-level analysis
        ngram_range=(1, 3),       # 1-3 character n-grams
        max_features=10000,       # Feature limit
        lowercase=True            # Normalize case
    )),
    ('classifier', LogisticRegression(
        random_state=42,          # Reproducible results
        max_iter=1000,           # Training iterations
        multi_class='multinomial' # Multi-class classification
    ))
])
```

### Feature Engineering
- **Character N-grams**: Captures phonetic patterns
- **Space Markers**: Preserves word boundaries
- **Lowercase Normalization**: Consistent processing
- **Special Character Removal**: Clean input data

## 📁 File Structure

### Project Layout
```
firstname_to_nationality/
├── .devcontainer/              # VS Code development container
│   ├── devcontainer.json      # Container configuration
│   └── Dockerfile             # Python 3.13 environment
├── .github/                   # GitHub configuration
│   └── instructions/          # Documentation
│       └── architecture.instruction.md
├── firstname_to_nationality/  # Main package
│   ├── __init__.py           # Package exports
│   ├── firstname_to_nationality.py  # Core implementation
│   ├── best-model.pt         # Trained model (binary)
│   └── firstname_nationalities.pkl  # Dictionary (binary)
├── example.py                # Usage examples
├── nationality_trainer.py    # Training script
├── predict.py               # Prediction script
├── setup.py                 # Package installation
├── requirements.txt         # Dependencies
├── README.md               # Documentation
└── MANIFEST.in             # Package data files
```

### File Purposes

| File | Purpose | Type |
|------|---------|------|
| `firstname_to_nationality.py` | Core ML implementation | Source |
| `best-model.pt` | Trained model weights | Binary |
| `firstname_nationalities.pkl` | Name lookup dictionary | Binary |
| `nationality_trainer.py` | Model training utilities | Script |
| `example.py` | Usage demonstrations | Script |
| `predict.py` | Batch prediction script | Script |

## 🔧 Design Patterns

### 1. **Facade Pattern**
- `FirstnameToNationality` provides simple interface to complex ML pipeline
- Hides TF-IDF vectorization, model loading, preprocessing complexity

### 2. **Strategy Pattern**
- Dictionary lookup vs. ML model prediction
- Configurable via `use_dict` parameter

### 3. **Factory Pattern**
- `_create_default_model()` creates standardized ML pipeline
- Consistent model architecture across sessions

### 4. **Template Method Pattern**
- `__call__()` method defines prediction workflow
- Delegates to `predict_single()` for actual processing

## 🚀 Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Models loaded only when needed
2. **Batch Processing**: Support for multiple names simultaneously
3. **Dictionary Caching**: Fast lookup for common names
4. **Memory Efficiency**: joblib for model serialization

### Scalability Features
- **Mini-batch Support**: `mini_batch_size` parameter
- **Configurable Features**: TF-IDF parameters tunable
- **Extensible Architecture**: Easy to swap ML backends

## 🔒 Error Handling

### Graceful Degradation
```python
# Model loading fails → Create default model
# Dictionary missing → Empty dictionary (model-only mode)
# Prediction error → Return ("unknown", 0.0)
# Invalid input → Preprocessing handles edge cases
```

### Exception Hierarchy
- **ValueError**: Invalid training data
- **FileNotFoundError**: Missing model/dictionary files
- **RuntimeError**: Model training failures

## 🧪 Testing Strategy

### Unit Tests (Recommended)
```python
# Test cases to implement:
test_name_preprocessing()        # NamePreprocessor functionality
test_model_loading()            # Model persistence
test_dictionary_operations()    # Dictionary save/load
test_prediction_accuracy()      # Core prediction logic
test_batch_processing()         # Multiple name handling
test_training_workflow()        # Model training pipeline
```

### Integration Tests
- End-to-end prediction workflows
- Model training and persistence
- Dictionary operations
- Error handling scenarios

### API Extensions
```python
# Potential future methods:
.predict_with_metadata()     # Return additional info
.batch_train()              # Incremental learning
.export_model()             # Model format conversion
.validate_predictions()     # Accuracy assessment
```

## 📊 Dependencies

### Core Dependencies
```python
# Production
numpy>=1.25.0              # Numerical operations
scikit-learn>=1.3.0        # Machine learning pipeline
pandas>=2.0.0              # Data manipulation
joblib>=1.3.0              # Model serialization

# Development
pytest>=7.4.0              # Testing framework
black>=23.0.0              # Code formatting
mypy>=1.5.0                # Type checking
```

### Dependency Rationale
- **scikit-learn**: Mature, well-documented ML library
- **numpy**: Efficient numerical computations
- **pandas**: Data handling and CSV processing
- **joblib**: Optimized model serialization

## 🎯 Design Principles

### 1. **Simplicity**
- Single-class interface for most operations
- Sensible defaults for all parameters
- Clear method naming and documentation

### 2. **Reliability**
- Comprehensive error handling
- Fallback mechanisms for missing files
- Input validation and sanitization

### 3. **Performance**
- Efficient preprocessing pipeline
- Optimized feature extraction
- Memory-conscious design

### 4. **Maintainability**
- Type hints throughout codebase
- Comprehensive docstrings
- Modular, testable components

### 5. **Extensibility**
- Configurable model parameters
- Pluggable preprocessing components
- Clear extension points

## 🔧 Configuration

### Environment Variables (Optional)
```bash
# Override default paths
FIRSTNAME_NATIONALITY_MODEL_PATH=/custom/model.pt
FIRSTNAME_NATIONALITY_DICT_PATH=/custom/dict.pkl
```

### Runtime Configuration
```python
# Custom initialization
predictor = FirstnameToNationality(
    model_path="/custom/model.pt",
    dictionary_path="/custom/dict.pkl"
)
```

## 📈 Monitoring and Logging

### Logging Strategy
- **INFO**: Model loading, training progress
- **WARNING**: Missing files, fallback usage
- **ERROR**: Prediction failures, invalid inputs
- **DEBUG**: Detailed preprocessing steps

### Metrics to Track
- Prediction confidence scores
- Dictionary hit rates
- Model loading times
- Training convergence metrics

---

## 🔄 Version History

| Version | Changes | Architecture Impact |
|---------|---------|-------------------|
| 1.0.0 | Initial implementation | Complete rewrite from original |
| | Python 3.13 compatibility | Modern type hints and features |
| | scikit-learn backend | Replaced Flair dependency |
| | Clear variable naming | Improved code readability |

## 📚 References

- [scikit-learn Documentation](https://scikit-learn.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [TF-IDF Vectorization](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
- [Logistic Regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)