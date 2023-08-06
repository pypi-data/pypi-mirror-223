from django.contrib.sessions.models import Session
from django.urls.base import reverse
from wagtail.models import Page
from wagtail.tests.utils import WagtailPageTests

from lxp.models import AcademyPage, CoursePage, ModulePage, ActivityPage, QuizPage
from lxp.models.security import SecurityOptions


class CoursePageTestsFactory(WagtailPageTests):
    """
    Sets up RP, HP, Academy, Course, M, A, Q
    for LXP tests
    """
    root_page = None
    home_page = None
    academy_page = None
    course_page = None
    module_page = None
    activity_page = None

    def setUp(self):
        self.initPages()
        return super().setUp()

    def initPages(self):
        self.root_page = Page.objects.get(path="0001")
        self.home_page = Page.objects.get(path="00010001")

        self.academy_page = AcademyPage(title='Academy', slug='academy')
        self.home_page.add_child(instance=self.academy_page)
        self.academy_page.save_revision().publish()

        self.course_page = CoursePage(
            title="Course",
            summary="Course A Summary",
            security=SecurityOptions.SECURITY_NONE,
        )
        self.academy_page.add_child(instance=self.course_page)
        self.course_page.save_revision().publish()

        self.module_page = ModulePage(
            title="Module 1",
            summary="Module 1 Summary",
        )
        self.course_page.add_child(instance=self.module_page)
        self.module_page.save_revision().publish()

        self.activity_page = ActivityPage(
            title="Activity 1",
            summary="Activity 1 Summary",
        )
        self.module_page.add_child(instance=self.activity_page)
        self.activity_page.save_revision().publish()

        self.quiz_page = QuizPage(
            title="Quiz 1",
            summary="Quiz 1 Summary",
        )
        self.module_page.add_child(instance=self.quiz_page)
        self.quiz_page.save_revision().publish()


    def testCorePages(self):
        Session.objects.all().delete()
        self.assertEqual(self.home_page.url_path, "/home/")
        self.assertEqual(self.home_page.slug, "home")

        self.assertEqual(self.academy_page.url_path, "/home/academy/")

        path_cutoff = len(self.home_page.url_path)
        rpath = reverse("wagtail_serve", args=(self.academy_page.url_path[path_cutoff:],))
        self.assertEqual(rpath, "/academy/")

        response = self.client.get(rpath)
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/academy/course/")
        self.assertContains(response, "Course A Summary", status_code=200)
