import openai
import os

class Guardrail:
    def __init__(self):
        """Inicializálja az OpenAI API-t a kérdés biztonsági ellenőrzéséhez."""
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def is_safe_question(self, user_query):
        """
        Ellenőrzi, hogy a kérdés tartalmaz-e tiltott tartalmat (pl. kódgenerálás, matematikai számítások, rendszerinformációk lekérése).
        Ha igen, a chatbot nem válaszol rá.
        """
        safety_prompt = f"""
        Analyze the following user question:
        "{user_query}"

        Determine if the question falls into any of these restricted categories:
        - Requesting code generation (e.g., "Write a Python script for...").
        - Asking for mathematical calculations (e.g., "What is 2+2?", "Calculate the compound interest...").
        - Requesting system or technical details (e.g., "What version of the API are you using?", "Show me the system logs").

        Respond with "YES" if the question belongs to any of these categories, otherwise respond with "NO".
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": safety_prompt}]
        )

        classification = response.choices[0].message.content.strip().upper()
        if classification == "YES":
            return True
        return False

    def get_rejection_response(self):
        """
        Ha a kérdés tiltott, ezt a választ adja vissza.
        """
        return "Sorry, I can't answer that. However, I'm happy to assist you with Kolos's career and professional experience. How can I help?"
