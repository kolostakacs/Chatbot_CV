import os
import openai
from collections import deque
from .query_db import QueryDatabase  # Import the vector search component
from .semantic_router import SemanticRouter  # 💡 Importáljuk a routert
from .guardrail import Guardrail  # 🔹 Importáljuk a biztonsági ellenőrzést
from .follow_up_manager import FollowUpManager

import concurrent.futures  # Párhuzamos futtatás


class LLMHandler:
    def __init__(self, db_url):
        """
        Initializes the LLM handler with a vector database connection and chat history.

        :param db_url: PostgreSQL database URL for vector search.
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.chat_history = [] # Stores the last 3 conversations
        self.db = QueryDatabase(db_url)  # Vector search instance
        self.router = SemanticRouter()
        self.guardrail = Guardrail()  # 🔹 Guardrail beépítése
        self.follow_up_manager = FollowUpManager(db_url)  # 🔥 ÚJ: FollowUpManager beépítése

    def format_response(self, raw_text):
        """
        A kapott nyers választ vizuálisan kiemeli és formázza.
        """
        format_prompt = f"""
        Your task is to transform the following chatbot response into a **visually appealing, engaging, and structured** format.
        Ensure that it remains **clear, professional, and easy to read**, without excessive decoration.
    
        **🔹 Guidelines for Formatting:**
        - **Use bold** to emphasize key points.
        - Use **emojis sparingly and meaningfully** (💡, 🚀, 🔥, 📈, 💼, ✅, 🎯) to enhance readability.
        - If the response includes a **list**, format it dynamically:
            - **Use "–" (dash) instead of bullets** for lists.
            - **Numbered lists (1️⃣, 2️⃣, 3️⃣) only for sequential steps.**
            - **Highlight key takeaways compactly** if they are grouped.
        - Keep it **concise, skimmable, and elegant**.
        - If a **strong statement** is present, format it for impact, but avoid overuse.
        - **DO NOT** overuse dividers (**—**) unless necessary.
        - **Vary formatting styles** to keep it fresh.
        
        ---
        
        **Raw Text to Format:**
        {raw_text}

        Now return a **well-structured** and **engaging** formatted response.
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Format this chatbot response in a visually structured way."},
                {"role": "user", "content": format_prompt}
            ]
        )

        return response.choices[0].message.content  # Formázott szöveg

    def ask_chatbot(self, user_query):
        """
        A chatbot válasza Kolos önéletrajzával és karrierjével kapcsolatos kérdésekre.
        """

        # **🔹 1. Biztonsági ellenőrzés (Guardrail)**
        if self.guardrail.is_safe_question(user_query):
            follow_up_questions = self.follow_up_manager.get_follow_up_questions(user_query)
            return self.guardrail.get_rejection_response(), follow_up_questions

        # **🔹 2. Általános kérdések kiszűrése**
        if self.router.is_general_question(user_query):
            follow_up_questions = self.follow_up_manager.get_follow_up_questions(user_query)
            return self.router.get_general_response(user_query), follow_up_questions

        # **🔹 3. Párhuzamos keresés: releváns chunkok és következő kérdések**
        with concurrent.futures.ThreadPoolExecutor() as executor:
            search_chunks_future = executor.submit(self.db.search_similar_texts, user_query, 5)
            followup_questions_future = executor.submit(self.follow_up_manager.get_follow_up_questions, user_query)

            search_results = search_chunks_future.result()
            follow_up_questions = followup_questions_future.result()

        # **🔹 4. Ha nincs találat, fallback opció használata**
        if not search_results:
            return "I couldn't find relevant information. Can you rephrase your question?", follow_up_questions

        # **🔹 5. Kiválasztjuk a top 5 chunkot a válasz generálásához**
        relevant_texts = "\n".join([result[0] for result in search_results])

        # **🔹 6. Előzmények formázása**
        history_context = "\n".join([f"User: {entry[0]}\nAssistant: {entry[1]}" for entry in self.chat_history[-3:]])

        # **🔹 7. Végső prompt összeállítása**
        prompt = f"""You are Kolos' personal assistant, answering questions on his behalf about his resume and career. 
        Keep your response concise and to the point, within 5-8 sentences. Always respond in English.
        Structure your response clearly, using:
        - **Bold titles**
        - ✅ Bullet points with checkmarks
        - 🏆 Highlight achievements
        - 📝 Separate sections if needed

        --- Conversation History ---  
        {history_context}  
        ----------------------------

        --- Relevant Sources ---  
        {relevant_texts}  
        ------------------------

        Question: {user_query}

        Answer:
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are Kolos' personal assistant, answering questions about his resume and career."},
                {"role": "user", "content": prompt}
            ]
        )

        assistant_reply = response.choices[0].message.content

        # **🔹 8. Chat history mentése**
        self.chat_history.append((user_query, assistant_reply))

        formatted_response = self.format_response(assistant_reply)

        return formatted_response, follow_up_questions

