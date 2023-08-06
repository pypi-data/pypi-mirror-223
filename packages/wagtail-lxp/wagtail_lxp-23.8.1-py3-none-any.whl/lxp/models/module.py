from cjkcms.models.cms_models import CjkcmsWebPage
from cjkcms.utils import get_richtext_preview
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import (
    FieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail.fields import RichTextField
from wagtail.search import index

from .activity import ActivityPage
from .quiz import QuizPage


class ModulePage(RoutablePageMixin, CjkcmsWebPage):
    """Learning module in a course."""

    class Meta:
        verbose_name = _("Module (Topic) Page")

    # needed only to avoid crash in backend preview
    template = "lxp/pages/module_page.html"

    parent_page_types = ["lxp.CoursePage"]
    subpage_types = ["lxp.ActivityPage", "lxp.QuizPage"]

    summary = RichTextField(
        blank=True, help_text="Brief summary for the course overview page"
    )
    description = RichTextField(
        blank=True, help_text="Full description for single-module view Page"
    )

    search_name = _("E-course module")
    search_name_plural = _("E-course modules")
    search_filterable = True

    content_panels = CjkcmsWebPage.content_panels + [
        FieldPanel("summary"),
        FieldPanel("description", classname="full"),
    ]

    @property
    def body_preview(self):
        if self.summary:
            return get_richtext_preview(self.summary)
        return get_richtext_preview(self.description) if self.description else ""

    search_fields = CjkcmsWebPage.search_fields + [
        index.SearchField("summary"),
    ]

    @property
    def course_page(self):
        return self.get_parent().specific

    @property
    def activities(self):
        return self.get_activities()

    def get_activities(self):
        """@todo: make consistent get_X() or X in course, module, activity, quiz"""
        return ActivityPage.objects.descendant_of(self).live()

    @property
    def quizzes(self):
        return self.get_quizzes()

    def get_quizzes(self):
        """@todo: make consistent get_X() or X in course, module, activity, quiz"""
        return QuizPage.objects.descendant_of(self).live()

    def serve(self, request, *args, **kwargs):
        """Override the default serve method to redirect to the parent course page."""
        return redirect(self.course_page.url)
