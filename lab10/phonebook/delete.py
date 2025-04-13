import psycopg2
from config import load_config

def delete_by_name(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor()as cur:
                cur.execute("DELETE FROM PhoneBook WHERE user_name = %s", (name,))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete_by_phone(phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor()as cur:
                cur.execute("DELETE FROM PhoneBook WHERE phone = %s", (phone,))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def delete_by_id(id):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor()as cur:
                cur.execute("DELETE FROM PhoneBook WHERE id = %s", (id,))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

select = input("Delete by:\nI - by id\nN - by name\nP - by phone\n")

if select == "I":
    id = int(input("ID: "))
    delete_by_id(id)
elif select == "N":
    name = input("Name: ")
    delete_by_name(name)
elif select == "P":
    phone = input("Phone: ")
    delete_by_phone(phone)