import psycopg2
from config import load_config
def create_tables():
    """I will create the table which called PhoneBook"""
    command = """CREATE TABLE PhoneBook(
                    user_name VARCHAR(150) NOT NULL,
                    phone VARCHAR(12) NOT NULL,
                    id SERIAL NOT NULL PRIMARY KEY
               )"""
    
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
    
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__=='__main__':
    create_tables()

#I've run it in order to create the table PhoneBook

#I can check it using these actions: 
#on the terminal: psql -U postgres
#then password: password
#then: \c labwork
# then: \d  