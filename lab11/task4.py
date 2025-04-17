import psycopg2
from config import load_config

def query(limit, offset):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("select get_paginated_records(%s, %s)", (limit, offset))
                result = cur.fetchall()
                print(result)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

limit, offset = input("Enter limit and offset: ").split()
query(limit, offset)