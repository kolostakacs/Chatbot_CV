import os
import openai
import psycopg2
from dotenv import load_dotenv

# PostgreSQL adatbázis elérési útvonala
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/.env"))
load_dotenv(dotenv_path)

# PostgreSQL kapcsolat
DB_URL = os.getenv("DB_URL")

# OpenAI API kulcs betöltése környezeti változóból
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_embedding(text):
    """
    Generál egy embedding vektort egy adott szöveghez az OpenAI API segítségével.
    """
    client = openai.OpenAI()  # Az új API szerint inicializálni kell egy OpenAI klienst
    response = client.embeddings.create(
        input=text,  # Most már simán stringként kell megadni
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding


def search_similar_text(search_text):
    """
    Keres a PGVector adatbázisban a legjobban illeszkedő szövegre.
    """
    embedding = get_embedding(search_text)

    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    query = """
    SELECT text, 1 - (embedding <=> %s::vector) AS similarity
    FROM text_vectors
    ORDER BY similarity DESC
    LIMIT 1;
    """

    cursor.execute(query, (embedding,))
    result = cursor.fetchone()

    conn.close()

    if result:
        print(f"🔎 Legjobb találat: {result[0]} (Hasonlóság: {result[1]:.4f})")
    else:
        print("❌ Nem találtunk releváns választ.")


# Teszt kérdés
search_text = "What is your education like?"
search_similar_text(search_text)