# from django.test import TestCase
from cjkcms.models import WebPage
from wagtail.models import Page
from wagtail.tests.utils import WagtailPageTests

from lxp.models import AcademyPage, CoursePage, ModulePage, ActivityPage


class AcademyPageTests(WagtailPageTests):
    """Tests for Academy Model & Page"""

    def test_can_create_an_academy_page_under_home(self):
        self.assertCanCreateAt(parent_model=WebPage, child_model=AcademyPage)

    def test_cannot_create_academy_under_course(self):
        self.assertCanNotCreateAt(parent_model=CoursePage, child_model=AcademyPage)

    def test_cannot_create_academy_under_module(self):
        self.assertCanNotCreateAt(parent_model=ModulePage, child_model=AcademyPage)

    def test_cannot_create_academy_under_activity(self):
        self.assertCanNotCreateAt(parent_model=ActivityPage, child_model=AcademyPage)

    def test_creating_academy_page(self):
        home_page = Page.objects.get(path="00010001")

        academy_page = AcademyPage(title='Academy', slug='academy')
        home_page.add_child(instance=academy_page)
        academy_page.save_revision().publish()

        self.assertEqual(academy_page.title, "Academy")
