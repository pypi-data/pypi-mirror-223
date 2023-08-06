from django.db import models

from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel,
)
from modelcluster.fields import ParentalKey

from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)

from lxp.models.course import CoursePage
from lxp.models.quiz_attempt import QuizAttempt
from django.utils.html import strip_tags


@register_snippet
class Topic(models.Model):
    """Topic (track) model"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)
    summary = RichTextField(blank=True, help_text="Brief summary for the overview page")
    description = RichTextField(
        blank=True, help_text="Optional full description for Topics Index Page"
    )
    is_featured = models.BooleanField(
        default=False, help_text="Activate to show on the Home Page"
    )
    topic_image = models.ForeignKey(
        "wagtailimages.Image",  # noqa
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    sort_order = models.IntegerField(default=0, blank=False, null=False)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("summary"),
        FieldPanel("description"),
        FieldPanel("is_featured"),
        FieldPanel("topic_image"),
        FieldPanel("sort_order"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Learning Topic"
        verbose_name_plural = "Learning Topics"


class CoursePageTag(TaggedItemBase):
    content_object = ParentalKey("CoursePage", related_name="course_tags")


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class TopicAdmin(ModelAdmin):
    model = Topic
    menu_icon = "list-ul"  # change as required
    list_display = ("name", "slug", "summary", "is_featured", "sort_order")
    list_filter = ["is_featured"]
    search_fields = ["name", "slug", "summary", "description"]
    prepopulated_fields = {"slug": ("name",)}


class CourseAdmin(ModelAdmin):
    model = CoursePage
    menu_icon = "folder-open-inverse"  # change as required
    menu_order = 100  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = (
        False  # or True to exclude pages of this type from Wagtail's explorer view
    )
    list_display = ("title", "summary_100", "security")
    list_filter = ("topics", "security", "enrollment")
    search_fields = ("title", "summary", "description")

    def summary_100(self, obj):
        """return trimmed version of the column, stripped of html tags"""
        s = strip_tags(obj.summary)
        return f"{s[:100]}..." if len(s) > 100 else s

    summary_100.short_description = "Brief summary"


class QuizAttemptAdmin(ModelAdmin):
    model = QuizAttempt
    menu_icon = "tick"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("quiz", "score", "session_key", "created")
    list_filter = ("quiz", "created", "user")
    search_fields = "user"


class AcademyAdmin(ModelAdminGroup):
    menu_label = "Academy"
    menu_icon = "openquote"
    menu_order = 200
    items = (CourseAdmin, TopicAdmin, QuizAttemptAdmin)



