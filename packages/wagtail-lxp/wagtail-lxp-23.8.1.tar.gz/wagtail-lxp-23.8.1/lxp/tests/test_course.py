# from django.test import TestCase
from wagtail.tests.utils import WagtailPageTests
from lxp.models import AcademyPage, CoursePage, ModulePage, ActivityPage
from cjkcms.models import WebPage

import wagtail_factories
from .lxp_factories import AcademyPageFactory, CoursePageFactory


class CoursePageTests(WagtailPageTests):
    """Tests for Course Model & Page"""

    def test_can_create_a_course_page(self):
        self.assertCanCreateAt(parent_model=AcademyPage, child_model=CoursePage)

    def test_cannot_create_a_course_under_home_page(self):
        self.assertCanNotCreateAt(parent_model=WebPage, child_model=CoursePage)

    def test_cannot_create_a_course_under_module_page(self):
        self.assertCanNotCreateAt(parent_model=ModulePage, child_model=CoursePage)

    def test_cannot_create_a_course_under_activity_page(self):
        self.assertCanNotCreateAt(parent_model=ActivityPage, child_model=CoursePage)

    def test_creating_course_page(self):
        root_page = wagtail_factories.PageFactory(parent=None)

        academy_page = AcademyPageFactory(parent=root_page)
        self.assertEqual(academy_page.title, "Academy")

        course_page = CoursePageFactory(parent=academy_page)
        self.assertEqual(course_page.title, "Course")

    def test_course_meta_description_shown(self):
        root_page = wagtail_factories.PageFactory(parent=None)
