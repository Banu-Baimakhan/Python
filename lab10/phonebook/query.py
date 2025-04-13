import psycopg2
from config import load_config

class Order_by:
    def __init__(self, obj):
        self.asc = f"SELECT id, user_name, phone FROM PhoneBook ORDER BY {obj}"
        self.desc = f"SELECT id, user_name, phone FROM PhoneBook ORDER BY {obj} DESC"

def select_order_by(obj, order):
    config = load_config()
    command = None
    if order == 0:
        command = Order_by(obj).asc
    else:
        command = Order_by(obj).desc
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                result = cur.fetchall()
                print(result)
            

        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def select_by_name(name):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, user_name, phone FROM PhoneBook WHERE user_name = %s", (name,))
                result = cur.fetchall()
                print(result)
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def select_by_phone(phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, user_name, phone FROM PhoneBook WHERE phone = %s", (phone,))
                result = cur.fetchall()
                print(result)
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def select_by_id(id):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, user_name, phone FROM PhoneBook WHERE id = %s", (id,))
                result = cur.fetchall()
                print(result)
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

def default_select():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor()as cur:
                cur.execute("SELECT id, user_name, phone FROM PhoneBook")
                result = cur.fetchall()
                print(result)
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

select = input("Choose mode:\nI - choose by id\nS - sorting\nN - choose by name\nP - choose py phone\nD - default select\n")
if select == 'S':
    ord = input("Order by: ")
    regime = int(input("Regime 0-ASC\n1-DESC\n"))
    select_order_by(ord, regime)
elif select == 'N':
    name = input("Name: ")
    select_by_name(name)
elif select == 'P':
    phone = input("Phone: ")
    select_by_phone(phone)
elif select == "I":
    id = int(input("ID: "))
    select_by_id(id)
else:
    default_select()