#!/usr/bin/env python3
"""Validate Bronze table data quality"""


def validate_schema(df):
    required_columns = [
        "job_id",
        "title",
        "company",
        "source",
        "location",
        "salary",
        "description",
        "url",
    ]
    existing_columns = df.columns
    missing = [col for col in required_columns if col not in existing_columns]
    if missing:
        print(f"❌ Missing columns: {missing}")
        return False
    print("✅ Schema validation passed")
    return True


def validate_data_quality(df):
    total = df.count()
    print(f"\n📊 Total records: {total}")

    # Check for nulls in required fields
    null_job_ids = df.filter(df.job_id.isNull()).count()
    null_titles = df.filter(df.title.isNull()).count()

    print(f"Null job_id: {null_job_ids} ({100*null_job_ids/total:.1f}%)")
    print(f"Null titles: {null_titles} ({100*null_titles/total:.1f}%)")

    if null_job_ids > 0:
        print("❌ Data quality issues found")
        return False

    print("✅ Data quality validation passed")
    return True


if __name__ == "__main__":
    print("🔍 Validating Bronze table...")
    print("Run this in Databricks notebook with Spark context")
