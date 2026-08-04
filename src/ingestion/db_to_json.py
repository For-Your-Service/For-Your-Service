import json
import os
import sys
import psycopg2
from datetime import datetime

def extract_and_convert():
    print("Initializing database extraction for Bronze ingestion...")
    
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "production_db")
    db_user = os.getenv("DB_USER", "admin")
    db_password = os.getenv("DB_PASSWORD", "secret")
    db_port = os.getenv("DB_PORT", "5432")

    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = connection.cursor()
        
        query = "SELECT id, payload_data, created_at FROM source_transactions WHERE processed = FALSE LIMIT 1000;"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        bronze_payloads = []
        for row in rows:
            record = {
                "record_id": row[0],
                "raw_content": row[1],
                "extracted_timestamp": datetime.utcnow().isoformat(),
                "source_system": "legacy_postgresql"
            }
            bronze_payloads.append(record)

        output_dir = "data/bronze"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"bronze_batch_{int(datetime.utcnow().timestamp())}.json")
        
        with open(output_file, "w") as f:
            json.dump(bronze_payloads, f, indent=2)
            
        print(f"Successfully extracted {len(bronze_payloads)} records to {output_file}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Database extraction failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    extract_and_convert()
