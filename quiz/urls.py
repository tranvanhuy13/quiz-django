from django.urls import path
from rest_framework.routers import DefaultRouter

from quiz.views import QuizViewSet


router = DefaultRouter()
router.register(r"questions", QuizViewSet, basename="quiz-questions")
urlpatterns = router.urls
