from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from .decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import UserActivity, QuizPage, QuizAttempt
import json


@ajax_required
@require_POST
@login_required
def switch_completed(request):
    """allows user to switch activity status as (un) completed"""
    req = json.loads(request.body)
    activity_id = req["id"]
    action = req["action"]

    if (not activity_id) or action != "switch":
        return JsonResponse({"status": "error 1"})
    try:
        ua = UserActivity.objects.get(activity_id=activity_id, user_id=request.user.id)
        ua.completed = not ua.completed
        ua.save()
        return JsonResponse({"status": "ok", "completed": ua.completed})
    except UserActivity.DoesNotExist:
        return JsonResponse({"status": "error 2"})


@ajax_required
@require_POST
def submit_quiz(request):
    """Processed quiz submission, saves an attempt, and returns score and (if allowed) detailed feedback"""
    req = json.loads(request.body)
    quiz_id = req["id"]
    answers = req["answers"]

    if not quiz_id:
        return JsonResponse({"status": "error 1"})

    try:  # use either logged in user id or session key
        if request.user.is_authenticated:
            user = request.user
            # this will allow easier retrieval of summaries - session_id will always contain either user or session key.
            session_id = user.id
        else:
            if not request.session.session_key:
                request.session.save()
            session_id = request.session.session_key
            user = None

        quiz = QuizPage.objects.get(id=quiz_id)
        score = quiz.calculate_score(answers)
        qa = QuizAttempt.objects.create(
            quiz=quiz, user=user, session_key=session_id, score=score, answers=answers
        )
        return JsonResponse({"status": "ok", "score": score, "feedback": None})
    except QuizPage.DoesNotExist:
        return JsonResponse({"status": "error 2"})


def quiz_summary(request, pk=0):
    '''returns quiz summary view for a given quiz page,
    with a distribution of summary results, and with
    distributions for each question'''
    quiz = QuizPage.objects.get(id=pk)
    if not quiz:
        raise Http404("Quiz not found")

    attempts = quiz.get_attempts()
    quiz.mark_content_items()
    items = quiz.get_content_items()
    answer_counts = quiz.get_distribution_of_answers()
    score_bins_all = quiz.get_score_bins()
    score_bins_best = quiz.get_score_bins(limit_to_best=True)
    print(answer_counts)

    return render(
        request,
        "lxp/admin/quiz/overall_summary.html",
        {
            "quiz": quiz,
            "pk": pk,
            "answer_counts": answer_counts,
            "score_bins_all": score_bins_all,
            "score_bins_best": score_bins_best,
        },
    )
