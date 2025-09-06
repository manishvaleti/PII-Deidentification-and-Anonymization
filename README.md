# PII Deidentification and Anonymization

This project provides tools to analyze, anonymize, and deidentify Personally Identifiable Information (PII) in CSV datasets using [Presidio](https://microsoft.github.io/presidio/) and [Faker](https://faker.readthedocs.io/en/master/).

## Features

- **Analyze**: Detect PII in CSV files and output analysis results.
- **Anonymize**: Replace detected PII with placeholder tags.
- **Deidentify**: Replace detected PII with realistic fake data using Faker.

## Project Structure

```
main.py                # Main script for analysis, anonymization, deidentification
data/
  pii_dataset.csv      # Input dataset with PII
  sample_df.csv        # Sample of 10 rows from input
output/
  analyzed_pii_dataset.csv     # Output: PII analysis results
  anonymized_pii_dataset.csv   # Output: Anonymized data
  deidentified_pii_dataset.csv # Output: Deidentified data
myenv/                 # Python virtual environment
```

## Requirements

- Python 3.10+
- Presidio Analyzer & Anonymizer
- Faker
- pandas

Install dependencies in your virtual environment:

```bash
source myenv/bin/activate
pip install presidio-analyzer presidio-anonymizer faker pandas
```

## Usage

1. Place your input CSV file in `data/pii_dataset.csv`.
2. Run the main script:

```bash
python main.py
```

3. Outputs will be saved in the `output/` directory.

## Functions

- `analyze_csv(df)`: Detects PII in each cell of the DataFrame.
- `anonymize_csv(df)`: Replaces PII with placeholder tags.
- `deidentify_text(text)`: Replaces PII in a string with fake data.
- `deidentify_csv(df)`: Applies deidentification to an entire DataFrame.

## Customization

- Update the `faker_mapping` dictionary in `main.py` to add or modify entity types and their fake data generators.

## License

MIT License
