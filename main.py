import pandas as pd
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from faker import Faker

df = pd.read_csv("./data/pii_dataset.csv")
sample_df = df.sample(n=10, random_state=1)
sample_df.to_csv("./data/sample_df.csv", index=False)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
fake = Faker()

faker_mapping = {
    "PERSON": lambda: fake.name(),
    "EMAIL_ADDRESS": lambda: fake.email(),
    "PHONE_NUMBER": lambda: fake.phone_number(),
    "LOCATION": lambda: fake.address().replace("\n", ", "),
    "US_SSN": lambda: fake.ssn(),
    "CREDIT_CARD": lambda: fake.credit_card_number()
}

#sample of 10
# analyze - write analyzed output to a file
# anonymize - write anonymized output to a file
# deidentify - write deidentified output to a file
#organize the functions accordingly
#one function to deidentify a single text input
#one function to deidentify a dataframe

def analyze_csv(df: pd.DataFrame) -> pd.DataFrame:
    analysis_results = []
    for i in range(len(df)):
        row_results = {}
        for col in df.columns:
            text = str(df.at[i, col])
            results = analyzer.analyze(text=text, language="en")
            row_results[col] = [r.to_dict() for r in results]
        analysis_results.append(row_results)
        
    return pd.DataFrame(analysis_results)

def anonymize_csv(df: pd.DataFrame) -> pd.DataFrame:
    df_ananymized = df.copy()
    for i in range(len(df_ananymized)):
        for col in df_ananymized.columns:
            text = str(df_ananymized.at[i, col])
            results = analyzer.analyze(text=text, language="en")
            if results:
                operators = {r.entity_type: OperatorConfig("replace", {"new_value": f'<{r.entity_type}>'}) for r in results}
                anonymized = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators)
                df_ananymized.at[i, col] = anonymized.text
    return df_ananymized

def deidentify_text(text: str) -> str:
    if not isinstance(text, str):
        return text

    results = analyzer.analyze(text=text, language="en")
    if not results:
        return text

    operators = {}
    for r in results:
        entity_type = r.entity_type
        if entity_type in faker_mapping:
            operators[entity_type] = OperatorConfig(
                "replace",
                {"new_value": faker_mapping[entity_type]()}
            )
        else:
            operators[entity_type] = OperatorConfig(
                "replace",
                {"new_value": "<REDACTED>"}
            )

    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results,
        operators=operators
    )
    return anonymized.text


### keep deidentify function only to deidentify. you pass some data, return defeidentified data.
def deidentify_csv(df: pd.DataFrame) -> pd.DataFrame:
    df_deidentified = df.copy()
    for i in range(len(df_deidentified)):
        for col in df_deidentified.columns:
            df_deidentified.at[i, col] = deidentify_text(df_deidentified.at[i, col])
    return df_deidentified

input_df = pd.read_csv("./data/sample_df.csv")

analyze_df = analyze_csv(input_df)
analyze_df.to_csv("./output/analyzed_pii_dataset.csv", index=False)
anonymized_df = anonymize_csv(input_df)
anonymized_df.to_csv("./output/anonymized_pii_dataset.csv", index=False)
deidentified_df = deidentify_csv(input_df)
deidentified_df.to_csv("./output/deidentified_pii_dataset.csv", index=False)
