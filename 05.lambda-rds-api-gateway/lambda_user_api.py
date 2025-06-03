import pymysql
import json
import os

# Database connection details from environment variables
DB_HOST = os.environ['DB_HOST']      # e.g., mydb.xxxxxx.us-east-1.rds.amazonaws.com
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']

# Connect to RDS MySQL
def connect_to_rds():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Main Lambda handler
def lambda_handler(event, context):
    try:
        method = event['httpMethod']
        if method == 'GET':
            return get_data()
        elif method == 'POST':
            return post_data(event)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# GET request handler
def get_data():
    connection = connect_to_rds()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            result = cursor.fetchall()
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
    finally:
        connection.close()

# POST request handler
def post_data(event):
    try:
        body = event.get('body')
        if not body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing request body'})
            }

        data = json.loads(body)
        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields: username or email'})
            }

        connection = connect_to_rds()
        try:
            with connection.cursor() as cursor:
                query = "INSERT INTO users (username, email) VALUES (%s, %s)"
                cursor.execute(query, (username, email))
                connection.commit()
                return {
                    'statusCode': 201,
                    'body': json.dumps({'message': f"User {username} added successfully"})
                }
        finally:
            connection.close()

    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
