# Import the built-in json module to handle serialization of Python dictionaries to JSON strings and files.
import json

# Import the built-in os module to interact with the underlying operating system and read environment variables.
import os

# Import the built-in sys module to access system-specific parameters and write error logs to standard error.
import sys

# Import the psycopg2 library to connect and execute SQL queries against a PostgreSQL database.
import psycopg2

# Import datetime from the datetime module to generate timestamps for our extracted audit payloads.
from datetime import datetime


def extract_and_convert():
    # Print an initial status message to standard output indicating the extraction process has started.
    print("Initializing database extraction for Bronze ingestion...")

    # Retrieve the database host from environment variables, defaulting to 'localhost' if not set.
    db_host = os.getenv("DB_HOST", "localhost")

    # Retrieve the database name from environment variables, defaulting to 'production_db' if not set.
    db_name = os.getenv("DB_NAME", "production_db")

    # Retrieve the database username from environment variables, defaulting to 'admin' if not set.
    db_user = os.getenv("DB_USER", "admin")

    # Retrieve the database password from environment variables, defaulting to 'secret' if not set.
    db_password = os.getenv("DB_PASSWORD", "secret")

    # Retrieve the database port from environment variables, defaulting to '5432' if not set.
    db_port = os.getenv("DB_PORT", "5432")

    try:
        # Establish a secure live connection to the PostgreSQL database using the extracted credentials.
        connection = psycopg2.connect(
            host=db_host, database=db_name, user=db_user, password=db_password, port=db_port
        )

        # Create a database cursor object to execute SQL commands and fetch result sets across the connection.
        cursor = connection.cursor()

        # Define the SQL query string to pull unProcessed records from the source transaction table, capping the batch size to 1000.
        query = "SELECT id, payload_data, created_at FROM source_transactions WHERE processed = FALSE LIMIT 1000;"

        # Execute the defined SQL query against the connected PostgreSQL database.
        cursor.execute(query)

        # Fetch all resulting rows from the executed cursor query into a local Python list.
        rows = cursor.fetchall()

        # Initialize an empty list to store the normalized records structured for Bronze layer ingestion.
        bronze_payloads = []

        # Iterate over each individual row returned from the database query result set.
        for row in rows:
            # Construct a standardized dictionary representing a single raw event payload with tracking metadata.
            record = {
                "record_id": row[0],
                "raw_content": row[1],
                "extracted_timestamp": datetime.utcnow().isoformat(),
                "source_system": "legacy_postgresql",
            }

            # Append the structured record dictionary into our batch collection list.
            bronze_payloads.append(record)

        # Define the target directory path where local bronze JSON files will be temporarily stored.
        output_dir = "data/bronze"

        # Ensure that the target local directory path exists, creating it recursively if necessary.
        os.makedirs(output_dir, exist_ok=True)

        # Generate a unique file path for the output JSON batch using a UTC epoch timestamp integer.
        output_file = os.path.join(
            output_dir, f"bronze_batch_{int(datetime.utcnow().timestamp())}.json"
        )

        # Open the generated output file path in write mode ('w') using a context manager.
        with open(output_file, "w") as f:
            # Serialize the entire list of python dictionaries into formatted JSON text and write it directly to the file.
            json.dump(bronze_payloads, f, indent=2)

        # Print a confirmation message to standard output indicating the batch was successfully exported.
        print(f"Successfully extracted {len(bronze_payloads)} records to {output_file}")

        # Safely close the database cursor to release server-side resources.
        cursor.close()

        # Safely close the active database connection network socket.
        connection.close()

    # Catch any unexpected runtime errors or database connection exceptions during execution.
    except Exception as e:
        # Print a descriptive error message to standard error stream with the failure details.
        print(f"Database extraction failed: {e}", file=sys.stderr)

        # Terminate the script execution immediately with a non-zero exit status code indicating failure.
        sys.exit(1)


# Conditional check to ensure execution only runs directly when invoked as a script via python CLI.
if __name__ == "__main__":
    # Invoke the main database extraction and conversion workflow function.
    extract_and_convert()
