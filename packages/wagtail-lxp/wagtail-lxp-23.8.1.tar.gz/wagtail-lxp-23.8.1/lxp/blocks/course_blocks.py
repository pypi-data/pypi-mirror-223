from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from cjkcms.blocks.base_blocks import BaseBlock


class CourseListBlock(BaseBlock):
    """
    List of Courses
    """

    heading = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Heading"),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Title"),
    )
    description = blocks.RichTextBlock(
        features=["bold", "italic", "ol", "ul", "hr", "link", "document-link"],
        label=_("Description"),
        required=False,
    )
    courses = blocks.StreamBlock(
        [
            ("course", blocks.PageChooserBlock("lxp.CoursePage")),
        ],
        label=_("Courses"),
    )

    def get_context(self, request, parent_context=None, *args, **kwargs):
        context = super().get_context(
            request, parent_context=parent_context, *args, **kwargs
        )
        context["user"] = parent_context.get("request").user

        return context

    class Meta:
        template = "lxp/blocks/course_list_block.html"
        icon = "fa-tasks"
        label = _("LXP Courses")
