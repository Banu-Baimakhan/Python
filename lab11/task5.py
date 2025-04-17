import psycopg2
from config import load_config

def delete_record(name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("call deleting(%s, %s)", (name, phone))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

name, phone = input("Name: "), input("Phone: ")
delete_record(name, phone)