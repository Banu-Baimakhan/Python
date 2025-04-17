import psycopg2
import json
from config import load_config

def insert_many_users(user_data):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_many_users(%s);", (json.dumps(user_data),))
                conn.commit()
                print("Users inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

user_data = [
    {"name": "Alice", "phone": "1234567890"},
    {"name": "Bob", "phone": "0987654321"},
    {"name": "Charlie", "phone": "5555555555"}
]

insert_many_users(user_data)