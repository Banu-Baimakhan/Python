import psycopg2
from config import load_config

def update_name(old_name, new_name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE PhoneBook SET user_name = %s WHERE user_name = %s""", (new_name, old_name))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def update_phone(old_phone, new_phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""UPDATE PhoneBook SET phone = %s WHERE phone = %s""", (new_phone, old_phone))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

up = input("What would you update?\nU - user name\nP - phone\n")

if up == 'U':
    old_name, new_name = input("Who is? "), input("New name: ")
    update_name(old_name, new_name)
else:
    old_phone, new_phone = input("Old phone? "), input("New phone: ")
    update_phone(old_phone, new_phone)