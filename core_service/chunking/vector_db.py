import psycopg2
from psycopg2.extras import execute_values

class VectorDatabase:
    def __init__(self, db_name: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """
        Inicializálja a PostgreSQL kapcsolatot PGVector támogatással.

        :param db_name: Az adatbázis neve.
        :param user: A PostgreSQL felhasználónév.
        :param password: A felhasználó jelszava.
        :param host: Az adatbázis szerver címe (alapértelmezett: localhost).
        :param port: Az adatbázis portja (alapértelmezett: 5432).
        """
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS text_vectors (
            id SERIAL PRIMARY KEY,
            text_data TEXT NOT NULL,
            embedding VECTOR(1536) NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_vector(self, text: str, embedding: list):
        insert_query = "INSERT INTO text_vectors (text, embedding) VALUES %s"
        execute_values(self.cursor, insert_query, [(text, embedding)])
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


