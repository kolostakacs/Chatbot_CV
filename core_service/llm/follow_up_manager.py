from llm.query_db import QueryDatabase


class FollowUpManager:
    def __init__(self, db_path):
        """
        Kezeli a következő kérdéseket. Kapcsolódik az adatbázishoz a hasonló kérdések kereséséhez.
        :param db: Az adatbázis kapcsolat objektuma.
        """
        self.db_path = db_path
        self.fallback_questions = [
            "Why should I hire Kolos?",
            "What are Kolos's biggest achievements?",
            "What are Kolos's educational background?"
        ]

    def get_follow_up_questions(self, user_query):
        """
        Keres a legrelevánsabb következő kérdések között. Ha nincs találat, fallback kérdéseket ad vissza.
        :param user_query: A felhasználó eredeti kérdése.
        :return: A 3 legjobb következő kérdés listája.
        """
        db = QueryDatabase(self.db_path)
        follow_up_raw = db.search_similar_texts(user_query, 3)

        follow_up_questions = []
        for result in follow_up_raw:
            question = result[0].split("Válasz:")[0].strip()  # Levágjuk a választ
            question = question.replace("Kérdés:", "").strip()  # Eltávolítjuk a "Kérdés:" előtagot
            follow_up_questions.append(question)

        return follow_up_questions if follow_up_questions else self.fallback_questions

    def update_fallback_questions(self, new_questions):
        """
        Frissíti az alapértelmezett következő kérdéseket.
        :param new_questions: Az új kérdések listája.
        """
        if isinstance(new_questions, list) and len(new_questions) == 3:
            self.fallback_questions = new_questions
        else:
            raise ValueError("Fallback questions list must contain exactly 3 items.")