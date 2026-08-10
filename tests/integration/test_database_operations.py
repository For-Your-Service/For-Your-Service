"""Integration tests for database operations"""
import pytest
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


@pytest.fixture(scope="module")
def spark():
    """Create Spark session for testing"""
    return SparkSession.builder \
        .appName("integration_tests") \
        .getOrCreate()


def test_write_to_bronze_layer(spark):
    """Test writing data to bronze layer"""
    test_data = [{
        'job_id': 'TEST001',
        'title': 'Test Engineer',
        'company': 'Test Corp',
        'location': 'Greenville, SC',
        'data_source': 'test',
        'ingestion_timestamp': '2026-08-10T12:00:00'
    }]
    
    df = spark.createDataFrame(test_data)
    df.write.mode('append').saveAsTable('veteran_intake.bronze_jobs')
    
    # Verify write
    result = spark.table('veteran_intake.bronze_jobs') \
        .filter("job_id = 'TEST001'") \
        .count()
    
    assert result == 1


def test_bronze_to_silver_transformation(spark):
    """Test bronze to silver layer transformation"""
    # Create test bronze data
    bronze_data = [{
        'job_id': 'TEST002',
        'title': 'devops engineer',  # lowercase
        'company': 'Tech Corp',
        'location': 'greenville, sc',  # lowercase
        'data_source': 'test'
    }]
    
    bronze_df = spark.createDataFrame(bronze_data)
    
    # Apply silver layer transformations
    silver_df = bronze_df \
        .withColumn('title', F.initcap('title')) \
        .withColumn('location', F.initcap('location')) \
        .dropDuplicates(['job_id'])
    
    # Verify transformations
    result = silver_df.collect()[0]
    assert result['title'] == 'Devops Engineer'
    assert result['location'] == 'Greenville, Sc'


def test_deduplication(spark):
    """Test that duplicate job_ids are removed"""
    test_data = [
        {'job_id': 'DUP001', 'title': 'Job 1'},
        {'job_id': 'DUP001', 'title': 'Job 1 Duplicate'},
        {'job_id': 'DUP002', 'title': 'Job 2'}
    ]
    
    df = spark.createDataFrame(test_data)
    deduped = df.dropDuplicates(['job_id'])
    
    assert deduped.count() == 2
