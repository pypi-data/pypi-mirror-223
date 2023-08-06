from django.db import models
from django.utils.translation import gettext_lazy as _


class EnrollmentOptions(models.IntegerChoices):
    ENROLL_AUTOMATIC = 0, _("Enroll automatically on first visit")
    ENROLL_CONFIRM = 1, _("Enroll with confirmation")
    ENROLL_RESTRICTED = 2, _("Enrollment restricted to group(s)")
    ENROLL_BY_INVITATION = 4, _("Enroll by invitation")
    ENROLL_DISABLED = 64, _("Enrollment disabled")


# security levels (for NON-enrolled)
class SecurityOptions(models.IntegerChoices):
    SECURITY_NONE = 0, _("Full guest access")
    SECURITY_QUIZZES = 1, _("Quizzes require login")
    SECURITY_DOWNLOADS = 2, _("Downloads require login")
    SECURITY_CONTENTS = 4, _("Course content requires login")
    SECURITY_LIST = 8, _("Content list requires login")
    SECURITY_COURSE = 16, _("Course hidden from non-logged")
    SECURITY_GROUP = 32, _("Course hidden from user not in specific groups")
    # user may be logged in, but unless enrolled, we don't let them see it at all
    SECURITY_ENROLL = 64, _("Course hidden from non-enrolled")


class LXPPermissions:
    """
    default user permissions, until we implement the user-course permission map
    """

    default_user_permissions = {
        SecurityOptions.SECURITY_COURSE: True,
        SecurityOptions.SECURITY_LIST: True,
        SecurityOptions.SECURITY_CONTENTS: True,
        SecurityOptions.SECURITY_DOWNLOADS: True,
        SecurityOptions.SECURITY_QUIZZES: True,
    }
