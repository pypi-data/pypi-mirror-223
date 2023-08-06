import datetime

from cjkcms.models import CjkcmsWebPage
from cjkcms.utils import get_richtext_preview
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index

import lxp.models
from .security import SecurityOptions


class PDFBlock(blocks.StructBlock):
    """Content block for selection of a local PDF file"""

    class EmbedModesBlock(blocks.ChoiceBlock):
        """List of choices for PDF Embedding"""

        choices = [
            ("SIZED_CONTAINER", "Sized Container [Adobe Embed]"),
            ("IN_LINE", "In-line  [Adobe Embed]"),
            ("LIGHT_BOX", "Lightbox  [Adobe Embed]"),
            ("EMBED", "Object Embed [HTML]"),
            ("IFRAME", "IFRAME Embed [HTML]"),
        ]

    document = DocumentChooserBlock(help_text="Select a local PDF document")
    embed_mode = EmbedModesBlock(default="IN_LINE", help_text="Select embed mode")
    custom_style = blocks.CharBlock(required=False, help_text="Optional CSS style")

    class Meta:
        icon = "doc-full-inverse"


class ActivityPage(RoutablePageMixin, CjkcmsWebPage):
    """Learning Activity in a module"""

    _seo_description = None
    _body_preview = None

    class Meta:
        verbose_name = _("Activity Page")

    parent_page_types = ["lxp.ModulePage"]
    subpage_types = []

    # ajax_template = 'lxp/activity_ajax/activity_completed.html'
    template = "lxp/pages/activity_page.html"

    # SVG Activity Icons
    class ActivityIcons(models.TextChoices):
        DEFAULT = "default.svg", _("Default")
        PDF = "pdf.svg", _("PDF Document")
        HTML = "html.svg", _("Richtext Content")
        WEBSITE = "website.svg", _("External web page")
        LOCAL_PAGE = "local_page.svg", _("Local web page")
        VIDEO_YOUTUTBE = "video_youtube.svg", _("Youtube video")
        VIDEO_VIMEO = "video_vimeo.svg", _("Vimeo video")

    # Activity model fields:
    summary = RichTextField(
        null=True, blank=True, help_text="Brief summary for the list of activities page"
    )
    icon = models.CharField(
        max_length=32, choices=ActivityIcons.choices, default=ActivityIcons.DEFAULT
    )
    publication_year = models.IntegerField(
        null=True, blank=True, default=datetime.datetime.now().year
    )
    content = StreamField(
        [
            ("rich_text", blocks.RichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
            # ('two_columns', TwoColumnBlock()),
            ("embedded_video", EmbedBlock(icon="media")),
            ("local_document", DocumentChooserBlock()),
            ("local_pdf", PDFBlock()),
            ("remote_pdf", blocks.URLBlock()),
            ("website_url", blocks.URLBlock()),
            ("local_page", blocks.PageChooserBlock()),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )
    content_length = models.IntegerField(
        null=True, blank=True, help_text="Videos: seconds. Texts: words"
    )

    # many-to-many with users (for tracking activities and scores)
    users = models.ManyToManyField("auth.User", through="UserActivity")

    content_panels = CjkcmsWebPage.content_panels + [
        FieldPanel("summary"),
        FieldPanel("icon"),
        FieldRowPanel(
            [
                FieldPanel("publication_year"),
                FieldPanel("content_length"),
            ]
        ),
        FieldPanel("content"),
        InlinePanel("related_links", label="Related links"),
        InlinePanel("related_authors", label="Activity authors"),
    ]

    @property
    def course_page(self):
        return self.get_ancestors().type(lxp.models.CoursePage).last().specific

    @property
    def module_page(self):
        return self.get_parent().specific

    @property
    def formatted_length(self):
        """If content length defined, checks if seconds or words and returns user-friendly format"""
        if not self.content_length:
            return None
        if self.icon.startswith("video"):
            return str(datetime.timedelta(seconds=self.content_length))
        else:
            minutes_reading = self.content_length // 275
        if minutes_reading == 0:
            return "< 1 minute"
        elif minutes_reading == 1:
            return "1 minute"
        else:
            return f"{str(minutes_reading)} minutes"

    # @TODO: move user_can_see to a separate utility class/module, and use it here!
    def user_can_see(self, security_level: SecurityOptions, user: User):
        return True

    def set_body_preview(self, user: User = None) -> str:
        if not self.user_can_see(SecurityOptions.SECURITY_LIST, user):
            self._body_preview = _(
                "This content is not available or you are not authorised to access it."
            )
            return self._body_preview or ""

        if self.summary:
            self._body_preview = get_richtext_preview(self.summary)
        return self._body_preview

    @property
    def body_preview(self):  # sourcery skip: assign-if-exp, reintroduce-else
        return self._body_preview or self.set_body_preview(None)

    @body_preview.setter
    def body_preview(self, value) -> None:
        if not self._body_preview:
            self._body_preview = value

    def set_seo_description(self, user: User = None) -> str:
        """
        Sets and returns seo description
        """
        self._seo_description = (
            self.search_description or self.set_body_preview(user)
            if self.user_can_see(SecurityOptions.SECURITY_LIST, user)
            else _(
                "This content is not available or you are not authorised to access it."
            )
        )
        return self._seo_description

        # if self.search_description:
        #     return self.search_description
        # if self.summary:
        #     return get_richtext_preview(self.summary, 200)
        # if self.content:
        #     return get_richtext_preview(self.content, 200)
        # return self.body_preview or ""

    @property
    def seo_description(self):
        return self._seo_description or self.set_seo_description(None)

    @seo_description.setter
    def seo_description(self, value) -> None:
        if not self._seo_description:
            self._seo_description = value

    search_fields = CjkcmsWebPage.search_fields + [
        index.SearchField("summary"),
    ]

    def update_user_activity_tracking(self, request):
        """If user logged in, increase the number of user visits to the page. Returns UA object"""
        if not request.user.is_authenticated:
            return None
        print(f"Activity: {self.title} - user {request.user.id}")
        try:
            ua = lxp.models.UserActivity.objects.get(
                activity_id=self.id, user_id=request.user.id
            )
            ua.visits = ua.visits + 1
            ua.save()
            return ua
        except lxp.models.UserActivity.DoesNotExist:
            self.users.add(request.user, through_defaults={"visits": 1})
            return self.useractivity_set.get(user=request.user)

    def get_fpnl_activity(self, course_modules):
        """
        Returns (f)irst, (p)revious, (n)ext, and (l)ast activity.
        Works also for activities in different modules
        """
        first_activity = None
        last_activity = None

        previous_activity = None
        next_activity = None
        activity_number = ""

        for m_index, m in enumerate(course_modules or []):
            for a_index, a in enumerate(m.activities.all()):
                if not first_activity:
                    first_activity = a

                if previous_activity and not next_activity:
                    next_activity = a

                if a.id == self.id:
                    previous_activity = a if a == first_activity else last_activity
                    activity_number = f"{m_index + 1}.{a_index + 1}"
                # rewrite in each iteration,
                # last_activity var can be reused in determining previous_activity
                last_activity = a

                # if next_activity:
                #     break

        # get rid of repeated values
        if previous_activity == self:
            previous_activity = None
        if first_activity == self:
            first_activity = None
        if next_activity == self:
            next_activity = None
        if last_activity == self:
            last_activity = None

        return [
            first_activity,
            previous_activity,
            next_activity,
            last_activity,
            activity_number,
        ]

    def get_context(self, request, *args, **kwargs):
        context = super(ActivityPage, self).get_context(request, *args, **kwargs)
        context["course_page"] = self.course_page
        context["module_page"] = self.module_page

        course_modules = self.course_page.get_modules(request.user)
        context[
            "modules"
        ] = course_modules  # what to do if user not logged in or has no privileges to see it
        (
            first_activity,
            previous_activity,
            next_activity,
            last_activity,
            activity_number,
        ) = self.get_fpnl_activity(course_modules)
        self.activity_number = activity_number
        context["first_activity"] = first_activity
        context["previous_activity"] = previous_activity
        context["next_activity"] = next_activity
        context["last_activity"] = last_activity
        context["activity"] = self
        context["site_root"] = self.get_url_parts()[1]
        # context['user'] = request.user if request.user.is_authenticated else None
        context["user_activity"] = self.update_user_activity_tracking(request)

        return context


class ActivityPageRelatedLink(Orderable):
    """At the bottom of each activity related links may be displayed"""

    page = ParentalKey(
        ActivityPage, on_delete=models.CASCADE, related_name="related_links"
    )
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldRowPanel(
            [
                FieldPanel("name"),
                FieldPanel("url"),
            ]
        )
    ]


class ActivityPageRelatedAuthor(Orderable):
    page = ParentalKey(
        ActivityPage, on_delete=models.CASCADE, related_name="related_authors"
    )
    name = models.CharField(max_length=128)
    country = models.CharField(null=True, blank=True, max_length=128)
    affiliation = models.CharField(null=True, blank=True, max_length=255)

    panels = [
        FieldRowPanel(
            [
                FieldPanel("name"),
                FieldPanel("country"),
            ]
        ),
        FieldPanel("affiliation"),
    ]
