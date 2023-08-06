from cjkcms.models import CjkcmsWebPage
from wagtail.fields import StreamField
from lxp.blocks import LXP_LAYOUT_STREAMBLOCKS


class LxpWebPage(CjkcmsWebPage):
    # Override body to provide custom content types
    body = StreamField(
        LXP_LAYOUT_STREAMBLOCKS, null=True, blank=True, use_json_field=True
    )

    # extends cjkcms default template without any overrides
    template = "lxp/pages/lxp_web_page.html"

    class Meta:
        verbose_name = "LXP Web Page"
