from django.urls import path
from django.conf.urls.i18n import i18n_patterns

from . import views

urlpatterns = [
    path('activity/completed/', views.switch_completed, name='switch_completed'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
]
