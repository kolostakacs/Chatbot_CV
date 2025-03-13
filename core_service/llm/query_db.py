import os
import openai
import psycopg2
from dotenv import load_dotenv

# Betöltjük a .env fájlt a backend könyvtárból
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/.env"))
load_dotenv(dotenv_path)

# PostgreSQL kapcsolat
DB_URL = os.getenv("DB_URL")


class QueryDatabase:
    def __init__(self, db_url: str):
        """
        Létrehozza az adatbázis kapcsolatot és előkészíti a keresést.
        """
        self.db_url = db_url
        self.conn = psycopg2.connect(self.db_url)
        self.cursor = self.conn.cursor()

    def search_similar_texts(self, search_text, top_k=5):
        """
        Keresés a vektor adatbázisban a legközelebbi 5 találatra.

        :param search_text: A keresési kérdés
        :param top_k: Az első `top_k` legjobban illeszkedő találat visszaadása
        :return: A legközelebbi találatok listája
        """
        # Embedding generálása
        embedding = openai.embeddings.create(
            input=[search_text],
            model="text-embedding-ada-002"
        ).data[0].embedding

        # SQL lekérdezés az 5 legközelebbi találatra
        query = """
        SELECT text, 1 - (embedding <=> %s::vector) AS similarity
        FROM text_vectors
        ORDER BY similarity DESC
        LIMIT %s;
        """

        self.cursor.execute(query, (embedding, top_k))
        results = self.cursor.fetchall()

        return results

    def close(self):
        """Lezárja az adatbázis kapcsolatot."""
        self.cursor.close()
        self.conn.close()
