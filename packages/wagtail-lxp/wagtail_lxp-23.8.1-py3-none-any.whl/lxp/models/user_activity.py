from django.db import models
from .activity import ActivityPage


class UserActivity(models.Model):
    """
    Intermediary model for relation users-to-activities (activity tracker).
    Used e.g. by lxpusers for reporting activity stats.
    """

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    activity = models.ForeignKey(ActivityPage, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    time_spent = models.PositiveIntegerField(
        default=0, help_text="Minutes spent in activity"
    )
    pct_score = models.PositiveIntegerField(
        default=0, help_text="Score in percent (where applicable, integer!)"
    )
    completed = models.BooleanField(
        default=False, help_text="Has activity been completed by user?"
    )
    visits = models.PositiveIntegerField(
        default=0, help_text="Number user visits in the activity"
    )

    class Meta:
        unique_together = ["user", "activity"]
