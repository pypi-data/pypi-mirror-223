import django.contrib.auth.models
from django.db import models
from django.db.models import ManyToManyField
from django.utils.translation import gettext_lazy as _
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from modelcluster.fields import ParentalManyToManyField
from django.forms import CheckboxSelectMultiple

from .module import ModulePage
from .activity import ActivityPage
from .user_activity import UserActivity
from .security import EnrollmentOptions, SecurityOptions, LXPPermissions
from cjkcms.models.cms_models import CjkcmsWebPage
from cjkcms.utils import get_richtext_preview
from wagtail.search import index


class CoursePage(CjkcmsWebPage):
    """LXP Single Course Page"""

    _seo_description = None
    _body_preview = None

    class Meta:
        verbose_name = _("Course Page")

    parent_page_types = ["lxp.AcademyPage"]
    subpage_types = ["lxp.ModulePage"]

    template = "lxp/pages/course_page.html"
    search_filterable = True
    search_name = _("E-course")
    search_name_plural = _("E-courses")

    summary = RichTextField(blank=True, help_text="Brief summary for the overview page")
    description = RichTextField(
        blank=True, help_text="Full description for course Index Page"
    )
    enrollment = models.IntegerField(
        choices=EnrollmentOptions.choices, default=EnrollmentOptions.ENROLL_AUTOMATIC
    )
    security = models.IntegerField(
        choices=SecurityOptions.choices, default=SecurityOptions.SECURITY_NONE
    )
    security_group = ManyToManyField("auth.group", blank=True)

    topics = ParentalManyToManyField("lxp.Topic", blank=True)

    navbar = models.BooleanField(
        default=True, help_text="Show side navbar for this course?"
    )

    content_panels = CjkcmsWebPage.content_panels + [
        FieldPanel("summary"),
        FieldPanel("description"),
        MultiFieldPanel(
            [FieldPanel("enrollment"), FieldPanel("security"),FieldPanel("security_group", widget=CheckboxSelectMultiple)],
            heading="Security and Enrollment",
        ),
        FieldPanel("topics", widget=CheckboxSelectMultiple),
        FieldPanel("navbar"),
    ]

    def set_body_preview(self, user: django.contrib.auth.models.User = None) -> str:
        if not self.user_can_see(SecurityOptions.SECURITY_COURSE, user):
            self._body_preview = _(
                "This content is not available or you are not authorised to access it."
            )
            return self._body_preview or ""

        if self.summary:
            self._body_preview = get_richtext_preview(self.summary)
        else:
            self._body_preview = (
                get_richtext_preview(self.description) if self.description else ""
            )
        return self._body_preview

    @property
    def body_preview(self):  # sourcery skip: assign-if-exp, reintroduce-else
        return self._body_preview or self.set_body_preview(None)

    @body_preview.setter
    def body_preview(self, value) -> None:
        if not self._body_preview:
            self._body_preview = value

    def set_seo_description(self, user: django.contrib.auth.models.User = None) -> str:
        """
        Sets and returns seo description
        """
        self._seo_description = (
            self.search_description or self.set_body_preview(user)
            if self.user_can_see(SecurityOptions.SECURITY_COURSE, user)
            else _(
                "This content is not available or you are not authorised to access it."
            )
        )
        return self._seo_description

    @property
    def seo_description(self):
        return self._seo_description or self.set_seo_description(None)

    @seo_description.setter
    def seo_description(self, value) -> None:
        if not self._seo_description:
            self._seo_description = value

    search_fields = CjkcmsWebPage.search_fields + [
        index.SearchField("summary"),
        index.SearchField("description"),
    ]

    @property
    def academy_page(self):
        return self.get_parent().specific

    def get_modules(self, user=None):
        return (
            ModulePage.objects.descendant_of(self).live()
            if self.user_can_see(SecurityOptions.SECURITY_LIST, user)
            else None
        )

    def get_activities_count(self, user=None):
        return (
            ActivityPage.objects.descendant_of(self).live().count()
            if self.user_can_see(SecurityOptions.SECURITY_LIST, user)
            else 0
        )

    def user_can_see(self, reqired_security_level: SecurityOptions, user):
        """
        Returns true if currently logged in user (or guest) has permission
        to see this course, it's modules, activities, etc.
        """
        if not user:
            return self.security < reqired_security_level
        if not user.is_authenticated:
            return self.security < reqired_security_level
        if self.security == SecurityOptions.SECURITY_GROUP \
            and not user.groups.filter(pk__in=self.security_group.all()).exists():
            return self.security < reqired_security_level
        if self.security >= reqired_security_level:
            return LXPPermissions.default_user_permissions[reqired_security_level]
        return self.security < reqired_security_level

    def get_user_activities_in_course(self, request):
        """If user logged in, get all tracked user activities in current course"""
        """ @TODO: fix or remove - it does not work, passes course rather than activity id"""
        if not request.user.is_authenticated:
            return None
        try:
            return UserActivity.objects.filter(
                activity_id=self.id, user_id=request.user.id
            )
        except UserActivity.DoesNotExist:
            return None

    def get_context(self, request, *args, **kwargs):
        context = super(CoursePage, self).get_context(request, *args, **kwargs)

        # @todo - skipping enrollment options, to implement!

        context["academy_page"] = self.academy_page
        self.body_preview = self.set_body_preview(request.user)
        self.seo_description = self.set_seo_description(request.user)
        if self.user_can_see(SecurityOptions.SECURITY_COURSE, request.user):
            context["course"] = self
        else:
            no_access_course = CoursePage(
                title=_("No Access"),
                summary=_("You are not authorised to access this course."),
                security=SecurityOptions.SECURITY_COURSE,
            )

            context["course"] = no_access_course
            context["security_error"] = True
        if self.user_can_see(SecurityOptions.SECURITY_LIST, request.user):
            context["modules"] = self.get_modules(request.user)
        context["activities_count"] = (
            self.get_activities_count()
            if self.user_can_see(SecurityOptions.SECURITY_LIST, request.user)
            else 0
        )

        return context
