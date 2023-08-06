from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from .course import CoursePage
from cjkcms.models.cms_models import CjkcmsWebPage


class AcademyPage(RoutablePageMixin, CjkcmsWebPage):  # type: ignore
    """LXP Academy Landing Page"""

    class Meta:
        verbose_name = _("LXP Academy Landing Page")

    description = RichTextField(null=True, blank=True)
    instruction_text = RichTextField(null=True, blank=True)
    instruction_file = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    list_visible = models.BooleanField(default=True, help_text="Show list of courses")

    content_panels = CjkcmsWebPage.content_panels + [
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("instruction_text"),
                FieldPanel("instruction_file"),
            ],
            heading="Instruction text and optional PDF attachment",
        ),
        FieldPanel("list_visible"),
    ]

    subpage_types = [
        "lxp.CoursePage",  # appname.ModelName
    ]

    template = "lxp/pages/academy_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super(AcademyPage, self).get_context(request, *args, **kwargs)
        context["courses"] = self.courses
        context["academy_page"] = self
        context["user"] = request.user  # required for permission check

        return context

    def get_courses(self):
        return CoursePage.objects.descendant_of(self).live()

    @route(r"^tag/(?P<tag>[-\w]+)/$")
    def course_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = "tag"
        self.search_term = tag
        self.courses = self.get_courses().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r"^topic/(?P<topic>[-\w]+)/$")
    def course_by_topic(self, request, topic, *args, **kwargs):
        self.search_type = "topic"
        self.search_term = topic
        self.courses = self.get_courses().filter(topics__slug=topic)
        return Page.serve(self, request, *args, **kwargs)

    @route(r"^$")
    def course_list(self, request, *args, **kwargs):
        self.courses = self.get_courses()
        return Page.serve(self, request, *args, **kwargs)
