import psycopg2
from config import load_config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__=="__main__":
    config = load_config()
    connect(config)

#I've run it in order to connect to the PostgreSQL, and I will use this code regularly in the further actions.