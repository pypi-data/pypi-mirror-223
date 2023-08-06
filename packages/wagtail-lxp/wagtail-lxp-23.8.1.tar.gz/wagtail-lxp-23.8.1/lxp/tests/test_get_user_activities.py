# from django.test import TestCase
import wagtail_factories
from django.test import RequestFactory
from wagtail.tests.utils import WagtailPageTests

from lxp.tests.lxp_factories import (
    AcademyPageFactory,
    CoursePageFactory,
    ModulePageFactory,
    ActivityPageFactory,
)
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sessions.models import Session
from django.test import Client


class UserActivityTests(WagtailPageTests):
    """Check if user activity is recorded"""
    user = None
    un = 'testuser1'
    up = '12345'

    def setUp(self):
        self.root_page = wagtail_factories.PageFactory(parent=None)
        self.academy_page = AcademyPageFactory(parent=self.root_page)
        self.course_page = CoursePageFactory(parent=self.academy_page)
        self.module_page = ModulePageFactory(parent=self.course_page)
        self.activity_page = ActivityPageFactory(parent=self.module_page)

    def test_creating_course_page(self):
        self.assertEqual(self.academy_page.title, "Academy")
        self.assertEqual(self.course_page.title, "Course")
        self.assertEqual(self.module_page.title, "Module")
        self.assertEqual(self.activity_page.title, "Activity")

    def test_anonymous_does_not_log_user_activity(self):
        # user not logged in, so no activity recorded
        Session.objects.all().delete()
        rf = RequestFactory()
        request = rf.get('/')
        request.user = AnonymousUser()

        ua = self.activity_page.update_user_activity_tracking(request)
        self.assertEqual(ua, None)

    def test_logged_in_generates_user_activity_with_visit_count(self):
        Session.objects.all().delete()

        # create a test user
        self.user = User.objects.create_user(username=self.un, password=self.up)
        self.user.save()

        self.logged_in_user = Client()
        self.logged_in_user.login(username=self.un, password=self.up)

        response = self.logged_in_user.get(self.course_page.url)
        # need to manually update activity tracker,
        # because we are on COURSE not ACTIVITY page
        ua = self.activity_page.update_user_activity_tracking(response.wsgi_request)
        self.assertEqual(ua.user, self.user)
        self.assertEqual(ua.activity, self.activity_page)
        self.assertEqual(ua.visits, 1)

        # check for increased visits counter in UA
        response = self.logged_in_user.get(self.course_page.url)
        ua = self.activity_page.update_user_activity_tracking(response.wsgi_request)
        self.assertEqual(ua.visits, 2)

