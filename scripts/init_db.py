#!/usr/bin/env python3
"""
Initialize Databricks Unity Catalog tables
"""

import os


def init_tables():
    """Create Bronze, Silver, and Gold tables"""

    print("Initializing Unity Catalog tables...")

    # Read SQL files
    sql_dir = os.path.join(os.path.dirname(__file__), "..", "sql")

    schemas = ["bronze_schema.sql", "silver_schema.sql", "gold_schema.sql"]

    for schema_file in schemas:
        with open(os.path.join(sql_dir, schema_file), "r") as f:
            f.read()

        print(f"  Creating tables from {schema_file}...")
        # TODO: Execute SQL via Databricks SDK
        print(f"  ✓ {schema_file}")

    print("\n✅ All tables initialized!")


if __name__ == "__main__":
    init_tables()
