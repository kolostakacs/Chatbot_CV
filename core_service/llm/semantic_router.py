import openai
import os


class SemanticRouter:
    def __init__(self):
        """Inicializálja az OpenAI API-t a kategorizáláshoz és válaszgeneráláshoz."""
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def is_general_question(self, user_query):
        """
        Ellenőrzi, hogy a kérdés általános-e (pl. időjárás, személyes állapot stb.).
        Ha igen, akkor egy statikus választ ad, és nem indít vektoros keresést.
        """
        classifier_prompt = f"""
        Classify the following user question:
        "{user_query}"

        Determine if it is a **general small talk question** (e.g., greetings, weather, personal well-being, jokes)
        OR a **relevant career-related question** about Kolos' **work, skills, achievements, or education**.
    
        - If it is about **weather, jokes, daily mood, small talk**, respond with **"YES"**.
        - If it is about **Kolos' career, skills, experience, education, job, projects, expertise**, respond with **"NO"**.
    
        Only return "YES" or "NO", nothing else.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": classifier_prompt}]
        )

        classification = response.choices[0].message.content.strip().upper()
        return classification == "YES"

    def get_general_response(self, user_query):
        """
        Ha a kérdés általános, egy LLM-et hív meg, amely barátságos választ ad, és megemlíti Kolos karrierjét.
        """
        general_prompt = f"""
        The user asked a general question: "{user_query}".

        Provide a friendly and engaging response to the question. 
        At the end of your response, include a sentence like: 
        "By the way, I can also assist you with Kolos' career and professional experience. How can I help with that?"

        Always answer in English.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": general_prompt}]
        )

        return response.choices[0].message.content

