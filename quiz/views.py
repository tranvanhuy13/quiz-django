import json

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import status

from quiz.models import Question, Session

from utils.quiz import Utils
class QuizViewSet(ViewSet):



    def retrieve(self, request, pk=None):
        try:
            q = Question.objects.get(id=pk)
            return Response(
                q.to_dict(), status=status.HTTP_200_OK
            )
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["post"], url_path="create-question")
    def create_questions(self, request):
        data = request.data
        content = data.get("content")
        q = Question(text=content)
        q.save()
        return Response(
            {"id": q.id, "text": q.text},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="get-questions")
    def get_questions(self, request):
        try:
            quiz = Utils.prepare_quiz(5)

            quiz_id = str(quiz.get("quiz_id"))
            questions = quiz.get("data").get("questions")
            quiz_id = 1
            # Store in DB
            Session.objects.create(
                quiz_id=quiz_id,
                data={"questions": questions}
            )

            res_question = Utils.remove_answer(questions)

            return Response({
                "quiz_id": quiz_id,
                "questions": res_question
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["post"], url_path=r'(?P<quiz_id>[^/.]+)/validate-question')
    def validate_question(self, request, quiz_id):
        # Step 1: Parse selected_option
        selected_option = request.data.get("selected_option")
        if selected_option is None:
            return Response({"error": "No selected option provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Get quiz by ID
        try:
            quiz = Session.objects.get(quiz_id=quiz_id)
        except Session.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Extract current question and answer
        data = quiz.data
        current_question = data.get("current_question", 0)  # Use default=0 here safely
        questions = data.get("questions")

        if not isinstance(questions, list) or current_question >= len(questions):
            return Response({"error": "Invalid or out-of-range question index"}, status=status.HTTP_400_BAD_REQUEST)

        correct_answer = str(questions[current_question].get("answer"))
        selected_option = str(selected_option)

        # Step 4: Validate answer
        is_correct = selected_option == correct_answer
        Utils.update_current_question(quiz_id)

        # Step 5: Prepare response
        response_data = {
            "correct_answer": correct_answer,
            "status": is_correct,
            "feedback": Utils.get_feedback(is_correct)
        }

        # Step 6: Update end time if last question
        if current_question == Utils.get_size(quiz_id) - 1:
            Utils.update_end_time(quiz_id)

        # Step 7: Append session log
        Utils.append_session(quiz_id, response_data)

        # Step 8: Return response
        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path=r'(?P<quiz_id>[^/.]+)/result')
    def result(self, request, quiz_id):
        try:
            quiz = Session.objects.get(quiz_id=quiz_id)
        except Session.DoesNotExist:
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

        data = quiz.data
        session_data = data.get("session", [])
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if not start_time or not end_time:
            return Response({"error": "Missing start or end time"}, status=status.HTTP_400_BAD_REQUEST)

        correct_answer = sum(1 for ans in session_data if ans.get("status"))
        total_questions = Utils.get_size(quiz_id)

        return Response({
            "time_seconds": round(end_time.timestamp() - start_time.timestamp(), 2),
            "correct_answer": correct_answer,
            "incorrect_answers": total_questions - correct_answer,
        }, status=status.HTTP_200_OK)