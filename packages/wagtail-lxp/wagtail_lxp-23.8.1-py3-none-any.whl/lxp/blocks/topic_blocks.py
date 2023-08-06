"""LXP-topics related Stream Blocks"""

from django.utils.translation import gettext_lazy as _
from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, RichTextBlock
from lxp.models import Topic, AcademyPage
from typing import List
from wagtail.blocks import PageChooserBlock


class FeaturedTopicsBlock(StructBlock):
    academy_page = PageChooserBlock(
        required=False, page_type="lxp.AcademyPage", label="Parent Academy Page"
    )
    name = CharBlock(label="Section Title", required=True)
    summary = RichTextBlock(required=False, features=["bold", "italic"])
    filter_featured = BooleanBlock(label="Only featured", required=False)

    def get_topics(self, featured_only: bool = False) -> List[Topic]:
        """Returns list of Topics, optionally limited to featured"""
        if featured_only:
            return Topic.objects.filter(is_featured=True).order_by("sort_order")
        else:
            return Topic.objects.all().order_by("sort_order")

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["featured"] = self.get_topics(request["filter_featured"])
        context["academy_page"] = (
            request["academy_page"] or AcademyPage.objects.live().first()
        )

        return context

    class Meta:
        # value_class = CourseStructValue
        template = "lxp/blocks/featured_topics_block.html"
        icon = "placeholder"
        label = _("LXP Topics")
