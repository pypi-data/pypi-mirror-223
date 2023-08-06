from django.db import models
from .quiz import QuizPage


class QuizAttempt(models.Model):
    """Log of Quiz attempts"""

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)
    quiz = models.ForeignKey(QuizPage, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(null=True)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}, {self.quiz} - {self.score}"

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
