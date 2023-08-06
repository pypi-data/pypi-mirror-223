from lxp.models import QuizAttempt
from django.db.models import Count, Min, Max


def get_best_quiz_attempt_by_ids(quiz_id: int, user_id: int):
    """Get QuizAttempt count and max score for a given quiz and user ids"""
    return QuizAttempt.objects.filter(quiz_id=quiz_id, user_id=user_id).aggregate(
        count=Count("quiz_id"),
        max=Max("score"),
        date_created=Min("created"),
        date_updated=Max("created"),
    )
