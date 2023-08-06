from typing import Optional

from django.template.defaulttags import register

from lxp.utils import get_best_quiz_attempt_by_ids
from ..models import UserActivity, CoursePage, SecurityOptions


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag()
def get_2d_item(dictio, key1, key2):
    print("D", len(dictio), "E", key1, key2)
    if key1 in dictio:
        if key2 in dictio[key1]:
            return dictio[key1][key2]
    else:
        return 0


@register.filter
def subtract(value, arg):
    return value - arg


@register.filter
def num2uc(value):
    """converts 1-based index into uppercase letters A,B..."""
    return chr(value + 64)


@register.filter
def is_tracked(activity, user_id):
    return activity.users.filter(useractivity__user_id=user_id).count() > 0


@register.simple_tag()
def get_ua(activity_id: int, user_id: int) -> Optional[UserActivity]:
    """Get UserActivity tracker for given activity and user ids"""
    try:
        return UserActivity.objects.get(activity_id=activity_id, user_id=user_id)
    except UserActivity.DoesNotExist:
        return None


@register.simple_tag()
def get_qa_stats(quiz_id: int, user_id: int):
    """Get QuizAttempt count and max score for a given quiz and user"""
    return get_best_quiz_attempt_by_ids(quiz_id, user_id)


@register.simple_tag()
def user_can_see(course, user, permission):
    """
    check if permissions is one of defined in SecurityOptions, and if so,
    return True if user has permission to see this course/list/activity, etc.
    Permissions are strings like "SECURITY_COURSE",
    "SECURITY_LIST" matching keys in SecurityOptions.
    """

    if not isinstance(course, CoursePage):
        return False
    # @TODO: I have no idea why in the test course is a string rather than a CoursePage
    if permission in SecurityOptions.__members__:  # type: ignore
        return course.user_can_see(getattr(SecurityOptions, permission), user)
    return False
