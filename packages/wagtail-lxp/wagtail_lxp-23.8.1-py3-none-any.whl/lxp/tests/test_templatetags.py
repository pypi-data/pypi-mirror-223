from django.test import TestCase
from django.template import engines
from lxp.templatetags.lxp_extras import get_item, subtract, num2uc
from wagtail.models import Site
from cjkcms.models import AdobeApiSettings

# from django.template import Context, Template


django_engine = engines["django"]


class NoContextFiltersTest(TestCase):
    """Unit tests for simple filters in lxp, not using context"""

    def test_get_item(self):
        val2 = {"a": "b"}
        dictionary = {"key1": "val1", "key2": val2}
        result = get_item(dictionary, "key2")
        self.assertEqual(result, val2)

    def test_subtract(self):
        result = subtract(5, 1)
        self.assertEqual(result, 4)

    def test_num2uc(self):
        self.assertEqual(num2uc(1), "A")
        self.assertEqual(num2uc(3), "C")

    def test_AdobeApiKeyInTemplate(self):
        site = Site.objects.filter(is_default_site=True)[0]
        adobe_api_key = AdobeApiSettings.for_site(site=site)
        adobe_api_key.adobe_embed_id = "test_key"
        adobe_api_key.save()

        rt = django_engine.from_string(
            "{% load wagtailsettings_tags %}{% get_settings use_default_site=True %}{{ settings.cjkcms.AdobeApiSettings.adobe_embed_id }}"
        ).render(None)
        self.assertEqual(
            rt, "test_key", "Adobe API key not returned in template context"
        )


# class ContextFiltersTest(TestCase):
#     ## need to pass context to make it work
#     def test_course_permission(self):
#         rt = django_engine.from_string(
#             "{% load lxp_extras %}{% course_permission course user 'see_course' as can_see_course %}{{ can_see_course }}"
#         ).render(None)
#         self.assertEqual(
#             rt, "danger", "map_to_bootstrap_alert for 'error' did not return 'danger'"
#         )
