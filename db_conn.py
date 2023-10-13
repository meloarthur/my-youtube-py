import psycopg2

def get_db_connection():
    connection = psycopg2.connect(
        dbname="my-youtube",
        user="postgres",
        password="admin",
        host="localhost",  # substitua pelo host do seu banco de dados
        port="5432"        # substitua pela porta do seu banco de dados
    )
    return connection
