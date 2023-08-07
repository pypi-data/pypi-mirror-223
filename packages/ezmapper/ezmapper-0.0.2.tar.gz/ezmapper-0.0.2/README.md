# 🌐 ezmapper

Welcome to `ezmapper` — a Python package that supercharges your Extract-Transform-Load (ETL) processes. With a core focus on an intuitive interface, ezmapper aids in seamlessly mapping data between various sources and destinations. Whether you love YAML or Excel for configurations, we've got you covered!

## 🚀 Installation

Getting started with `ezmapper` is a breeze:

```bash
pip install ezmapper
```

## 🌟 Features

- **Simplified ETL**: Seamlessly load and map data in pandas DataFrames.
- **Configuration Flexibility**: Whether you're a YAML enthusiast or a dictionary lover, configure the way you want!
- **Two-Way Mapping**: Apply mappings on your data or go the other way round.
- **Excel Enthusiast?**: Directly save your mappings to Excel or initialize them from an Excel sheet.

## 📚 Classes

### `Mapper`

The heart of `ezmapper`. Dive into the core ETL functionalities:

- Fetch mapping from a YAML or directly from a dictionary.
- Transform a pandas DataFrame using `load()` and revert transformations using `dump()`.
- Excel wizards, rejoice! Use `to_excel()` to save, or `from_excel()` to load configurations.

```python
from ezmapper import Mapper
```

## 💡 Example Usage

Given below is a concise YAML configuration for your understanding:

```yaml
config:
  comment_column: comment # Highlight changed values in the DataFrame
  id_column: id # For error logging & ensuring unique entries

filters:
  - 0.15 < floats < 1 # Applying filters on the DataFrame

mapping:
  id: A
  letters: B
  booleans: C
  floats:
    column: D
    rule_value: True -> floats * 10
  words: E
  timestamp:
    column: CREATE_COLUMN()
    default_value: pd.Timestamp.now()
  comment: CREATE_COLUMN()
```

## 🤝 Contributing

Got an idea? 🌱 Found a bug? 🐞

Join in! Open an issue or submit a pull request. Your contributions are heartily welcome.

## 📞 Support

Need a hand? Don't hesitate. Open an issue on the repository or drop a message to our dedicated maintainers.
