import json            # To parse JSON strings (for secrets)
import boto3           # AWS SDK for Python, used to interact with AWS services (Secrets Manager here)
import pymysql         # MySQL client library for Python

# Define the database and table names you want to create
new_db_name = "test"
table_name = "mytable"

# Function to retrieve the database credentials stored in AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client('secretsmanager')                  # Create a Secrets Manager client
    response = client.get_secret_value(SecretId=secret_name) # Retrieve the secret using the secret's name
    return json.loads(response['SecretString'])              # Parse the secret JSON string and return as dict

# Function to connect to the RDS instance using the retrieved secret credentials
def connect_to_rds(secret):
    connection = pymysql.connect(
        host=secret['host'],               # Hostname of the RDS instance (from secret)
        user=secret['username'],           # Username (from secret)
        password=secret['password'],       # Password (from secret)
        cursorclass=pymysql.cursors.DictCursor  # Return query results as dictionaries
    )
    return connection                    # Return the DB connection object

# Main Lambda function handler, triggered on Lambda invocation
def lambda_handler(event, context):
    secret_name = "dbsecrets"            # replace you Secrets Manager secret name containing DB credentials
    connection = None                   # Initialize connection variable

    try:
        # Retrieve DB credentials from AWS Secrets Manager
        secret = get_secret(secret_name)
        
        # Establish connection to the RDS database
        connection = connect_to_rds(secret)
        
        with connection.cursor() as cursor:
            # Create the database if it doesn't exist already
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            
            # Switch to the newly created (or existing) database
            cursor.execute(f"USE {new_db_name};")

            # Define SQL query to create a table if it doesn't exist
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,          -- Auto-increment primary key column 'id'
                name VARCHAR(255) NOT NULL,                 -- 'name' column, non-null string up to 255 chars
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Timestamp column defaults to current time
            );
            """
            # Execute the table creation query
            cursor.execute(create_table_sql)

        # Return success response
        return {
            'statusCode': 200,
            'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
        }

    except Exception as e:
        # Print and return the error message if anything fails
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        # Close the database connection if it was opened
        if connection:
            connection.close()
