from django.contrib.auth.models import User, Group
from django.contrib.sessions.models import Session

from lxp.models.security import SecurityOptions
from .pages_setup import CoursePageTestsFactory
from django.urls import reverse

class CoursePageTests(CoursePageTestsFactory):
    """Tests for Course Model & Page"""

    def setUp(self):
        # create a test user
        test_user1 = User.objects.create_user(username="testuser1", password="12345")
        test_user1.save()

        self.group22 = Group(name="students 2022")
        self.group22.save()
        test_user2 = User.objects.create_user(username="testuser2", password="12345")
        test_user2.groups.add(self.group22)
        test_user2.save()

        self.group23 = Group(name="students 2023")
        self.group23.save()
        test_user3 = User.objects.create_user(username="testuser3", password="12345")
        test_user3.groups.add(self.group23)
        test_user3.save()

        test_user4 = User.objects.create_user(username="testuser4", password="12345")
        test_user4.groups.add(self.group22)
        test_user4.groups.add(self.group23)
        test_user4.save()


        # this sets up RP, HP, AP, CP, MP, AP, QP
        return super().setUp()

    def testModuleRedirectsToCourse(self):
        Session.objects.all().delete()
        response = self.client.get("/academy/course/module-1/")
        self.assertRedirects(response, '/academy/course/', status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_protect_course_page_nologin(self):
        # not sure why, but by default a session is created for the test user
        Session.objects.all().delete()

        course_page = self.course_page
        # one security hole to patch is in page meta tags: even for a hidden course, description is visible

        course_page.security = SecurityOptions.SECURITY_COURSE
        course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # assert that "No access" is visible in the page
        response = self.client.get("/academy/course/")
        self.assertContains(response, "No access", status_code=200)

    def test_protected_course_page_login(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_COURSE
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser1", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)

    def test_protected_course_page_group_correct(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
        self.course_page.security_group.set([self.group23])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser3", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)

    def test_protected_course_page_group_different(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
        self.course_page.security_group.set([self.group23])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser2", password="12345")


       # assert that "No access" is visible in the page
        response = self.client.get("/academy/course/")
        self.assertContains(response, "No access", status_code=200)
    def test_protected_course_page_group_both(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
        self.course_page.security_group.set([self.group23])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser4", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)
    def test_protected_course_page_group_no_group_user(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
        self.course_page.security_group.set([self.group23])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser1", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)

    def test_protected_course_page_group_no_group_course_user(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
       # self.course_page.security_group.set([self.group23])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser1", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)

    def test_protected_course_page_group_two_group_course_one_user(self):
        Session.objects.all().delete()

        self.course_page.security = SecurityOptions.SECURITY_GROUP
        self.course_page.security_group.set([self.group23,self.group22])
        self.course_page.save()

        # assert that "Course Summary is not visible in the page"
        response = self.client.get("/academy/course/")
        self.assertNotContains(response, "Course A Summary", status_code=200)

        # login
        self.client.login(username="testuser3", password="12345")

        # assert that "Course Summary is not visible in the page"
        response = self.client.get(self.course_page.url)
        self.assertContains(response, "Course A Summary", status_code=200)