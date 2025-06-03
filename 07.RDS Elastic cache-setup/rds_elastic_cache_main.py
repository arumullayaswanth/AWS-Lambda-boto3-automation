# Import necessary libraries
import pymysql        # For connecting to MySQL (RDS)
import redis          # For interacting with Redis (ElastiCache)
import json           # For encoding/decoding cached data
import sys            # To handle command-line arguments

# 🔧 Redis configuration (ElastiCache endpoint)
redis_client = redis.Redis(
    host='dev-l6ap1d.serverless.use1.cache.amazonaws.com',  # Removed port from host(removed the port from the host string and kept the port parameter separate)
    port=6379,              # Default Redis port specified separately
    ssl=True,               # TLS enabled for AWS ElastiCache
    decode_responses=True,  # Ensures Redis returns strings, not bytes
    socket_timeout=5        # Optional timeout in seconds
)

# 🔧 RDS (MySQL) configuration
RDS_HOST = 'database-1.c0n8k0a0swtz.us-east-1.rds.amazonaws.com'  # Replace your RDS endpoint
RDS_USER = 'admin'           # MySQL username
RDS_PASSWORD = '9959148343'  # MySQL password
RDS_DB_NAME = 'test'         # Database name
TABLE_NAME = 'users'         # Table name to query

# 🔄 Function to fetch data from the RDS MySQL database
def fetch_data_from_rds():
    try:
        # Establish connection to RDS
        connection = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB_NAME
        )
        print("🔗 Connected to RDS")

        # Use cursor to execute SQL query
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 10;")  # Query top 10 records
            rows = cursor.fetchall()  # Fetch all results
            return rows

    except Exception as e:
        # Handle and print any connection or query errors
        print("❌ RDS Error:", e)
        return None

    finally:
        # Always close the connection if it was established
        if 'connection' in locals():
            connection.close()

# 🧠 Main function logic for cache-first strategy
def main():
    cache_key = 'cached_table_data'          # Redis cache key
    bypass_cache = "--refresh" in sys.argv   # Allow manual refresh by command-line flag

    # 🔎 Try to fetch from Redis cache (if not bypassing)
    if not bypass_cache:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            print("✅ Fetched from Redis cache:")
            print(json.loads(cached_data))  # Print JSON-decoded data
            return

    # 🛠 If no cache found or bypass requested, query the database
    print("⚙️ No cache found or refresh requested. Fetching from RDS...")
    data = fetch_data_from_rds()

    if data:
        # Store fresh data in Redis with an expiration time of 90 seconds
        redis_client.set(cache_key, json.dumps(data), ex=90)
        print("📦 Cached in Redis:")
        print(data)
    else:
        print("⚠️ No data fetched from RDS.")

# 🚀 Entry point for script execution
if __name__ == "__main__":
    main()
