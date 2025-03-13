from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv  # 🔥 .env fájl betöltése


# 🛠️ Core Service importálása (LLM_handler)
CORE_SERVICE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core_service"))
sys.path.append(CORE_SERVICE_PATH)

from llm.LLM_handler import LLMHandler  # Chatbot kezelő
from llm.follow_up_manager import FollowUpManager  # Follow-up kérdéskezelő

# 📌 Flask inicializálása
app = Flask(__name__)
CORS(app)  # Engedélyezi a frontend hozzáférést

load_dotenv()

# 🔥 Az adatbázis URL beolvasása a .env fájlból
DB_URL = os.getenv("DB_URL")
PORT=5000
DEBUG_MODE=True

# 🔥 LLMHandler és FollowUpManager inicializálása
chatbot = LLMHandler(DB_URL)
follow_up_manager = FollowUpManager(DB_URL)

@app.route('/chat', methods=['POST'])
def chat():
    """
    🎯 API végpont a chatbothoz
    """
    try:
        # 📥 Beérkező adatok ellenőrzése
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message received!"}), 400

        # 🚀 Chatbot meghívása (válasz + javasolt kérdések)
        response, follow_up_questions = chatbot.ask_chatbot(user_message)

        # 📤 JSON válasz küldése
        return jsonify({
            "response": response,
            "follow_up_questions": follow_up_questions
        })

    except Exception as e:
        print(f"❌ Hiba történt a /chat végpontban: {e}")
        return jsonify({"error": "Internal server error"}), 500

# ✅ **ÚJ VÉGPONT: Alapértelmezett kérdések lekérése**
@app.route('/get_fallback_questions', methods=['GET'])
def get_fallback_questions():
    """
    🎯 API végpont az alapértelmezett (fallback) kérdések lekérdezésére.
    """
    return jsonify({"fallback_questions": follow_up_manager.fallback_questions})

# 🚀 Szerver indítása
if __name__ == '__main__':
    app.run(port=PORT, debug=DEBUG_MODE)



