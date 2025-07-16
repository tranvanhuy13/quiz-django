from datetime import datetime
from uuid import uuid4
import random

from django.db.models import Max

from quiz.models import Question, Session


class Utils:

    @staticmethod
    def remove_answer(questions):
        return [
            {
                "question": question.get("text"),
                "options": question.get("options")
            } for question in questions
        ]

    @classmethod
    def prepare_quiz(cls, ques_number: int):
        quiz_id = uuid4()
        generated_questions = cls.get_random_questions(ques_number)
        return {
            "quiz_id": quiz_id,
            "data": {
                "start_time": datetime.utcnow(),
                "end_time": None,
                "answers": [],
                "current_question": 0,
                "questions": generated_questions
            }
        }

    @staticmethod
    def get_random_questions(n):
        all_ids = list(Question.objects.values_list("id", flat=True))

        if not all_ids:
            return []

        # Randomly pick up to `n` unique IDs
        selected_ids = random.sample(all_ids, min(n, len(all_ids)))

        random_questions = Question.objects.filter(id__in=selected_ids)

        # Format as dicts (including answer for internal use)
        return [
            {
                "id": q.id,
                "text": q.text,
                "options": q.options,  # Assuming `q.options` is a list or JSON string
                "answer": q.answer
            }
            for q in random_questions
        ]
    @classmethod
    def get_quiz(cls,quiz_id):
        try:
            return Session.objects.get(quiz_id=quiz_id)
        except Session.DoesNotExist:
            return None


    @classmethod
    def update_current_question(cls, quiz_id):
        quiz_session = cls.get_quiz(quiz_id)
        if quiz_session:
            current_question = quiz_session.data.get("current_question", 0)
            quiz_session.data["current_question"] = current_question + 1
            quiz_session.save()

    @classmethod
    def get_feedback(cls, status):
        return "Correct" if status else "Incorrect"

    @classmethod
    def get_size(cls, quiz_id):
        quiz_session = cls.get_quiz(quiz_id)
        if quiz_session:
            return len(quiz_session.data.get("questions", []))
        return 0

    @classmethod
    def update_end_time(cls, quiz_id):
        quiz_session = cls.get_quiz(quiz_id)
        if quiz_session:
            quiz_session.data["end_time"] = datetime.utcnow()
            quiz_session.save()

    @classmethod
    def append_session(cls, quiz_id, response_data):
        quiz_session = cls.get_quiz(quiz_id)
        if quiz_session:
            answers = quiz_session.data.get("answers", [])
            answers.append(response_data)
            quiz_session.data["answers"] = answers
            quiz_session.save()
        else:
            raise ValueError("Quiz session not found")