import json
import boto3
import pymysql

# Define the database and table name
new_db_name = "test"
table_name = "mytable"

# Function to retrieve secret from AWS Secrets Manager
def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Function to connect to RDS using secret credentials
def connect_to_rds(secret):
    connection = pymysql.connect(
        host=secret['host'],       # Ensure your secret includes 'host'
        user=secret['username'],
        password=secret['password'],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Lambda function handler
def lambda_handler(event, context):
    secret_name = "dbsecret"  # Replace with your actual secret name
    connection = None

    try:
        # Get DB credentials from Secrets Manager
        secret = get_secret(secret_name)
        
        # Connect to RDS
        connection = connect_to_rds(secret)
        
        with connection.cursor() as cursor:
            # Create database if not exists
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_db_name};")
            cursor.execute(f"USE {new_db_name};")

            # Create table if not exists
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_sql)

        return {
            'statusCode': 200,
            'body': f"Database '{new_db_name}' and table '{table_name}' created successfully."
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }

    finally:
        if connection:
            connection.close()
