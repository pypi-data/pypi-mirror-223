from lxp.blocks.topic_blocks import FeaturedTopicsBlock
from lxp.blocks.course_blocks import CourseListBlock

from cjkcms.blocks import (
    CONTENT_STREAMBLOCKS,
    HeroBlock,
    GridBlock,
    CardBlock,
    CardGridBlock,
    SearchableHTMLBlock,
)
from django.utils.translation import gettext_lazy as _
from cjkcms.settings import cms_settings

cms_settings.CJKCMS_FRONTEND_TEMPLATES_BLOCKS["courselistblock"] = [
    ("lxp/blocks/course_list_block.html", "Horizontal, image 1/4, text 3/4"),
    ("lxp/blocks/course_list_block_h-4-8.html", "Horizontal, image 1/3, text 2/3"),
]

LXP_CONTENT_STREAMBLOCKS = CONTENT_STREAMBLOCKS + [
    ("learning_topics", FeaturedTopicsBlock()),
    ("courses", CourseListBlock()),
]

LXP_LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(LXP_CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    SearchableHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(LXP_CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        SearchableHTMLBlock(icon="code", form_classname="monospace", label=_("HTML")),
    ),
]
