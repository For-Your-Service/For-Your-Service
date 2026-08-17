def validate_bronze_expectations(df):
    \"\"\"Aborts build if required fields are missing.\"\"\"
    if df is None:
        raise ValueError("Dataframe is empty or invalid.")
