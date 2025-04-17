import psycopg2
from config import load_config

def get_record(pattern):
    config = load_config()
    try: 
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("select get_record(%s)", (pattern,))
                result = cur.fetchall()
                print(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)   

pattern = input("Enter pattern: ")
get_record(pattern)