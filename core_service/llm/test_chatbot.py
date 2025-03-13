from http.client import responses

from LLM_handler import LLMHandler
from dotenv import load_dotenv
import os

# PostgreSQL adatbázis elérési útvonala
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend/.env"))
load_dotenv(dotenv_path)

# PostgreSQL kapcsolat
DB_URL = os.getenv("DB_URL")
chatbot = LLMHandler(DB_URL)

print("\n🤖 **Kolos Asszisztens** | Írj egy kérdést! (Kilépéshez: 'exit')")

while True:
    # Felhasználói kérdés bekérése
    user_query = input("\n🔹 Kérdésed: ")

    if user_query.lower() == "exit":
        print("👋 Kilépés... Viszlát!")
        break

    # Chatbot válaszának lekérdezése
    result = chatbot.ask_chatbot(user_query)

    # Eredmény kiírása
    print("\n🔎 **Legjobb találatok a vektor adatbázisból:**")
    search_results = chatbot.db.search_similar_texts(user_query)

    response, follow_up_questions = result
    print(f"📌 DEBUG: A chatbot visszatérési értéke: {result}")
    print(f"📌 Típus: {type(result)}")
    print(f"📌 Hossz: {len(result)}" if isinstance(result, tuple) else "❌ Nem tuple!")

    if search_results:
        for idx, text in enumerate(search_results, 1):
            print(f"{idx}. {text}")
    else:
        print("❌ Nem találtunk releváns találatot az adatbázisban.")

    print("\n🤖 **Chatbot válasza:**")
    print(response)
    if follow_up_questions:
        print("\n🔎 **Javasolt további kérdések:**")
        for idx, question in enumerate(follow_up_questions, 1):
            print(f"{idx}. {question}")
