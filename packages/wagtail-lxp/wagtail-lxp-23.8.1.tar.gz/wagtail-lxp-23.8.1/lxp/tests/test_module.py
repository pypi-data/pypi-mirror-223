from django.contrib.sessions.models import Session
from .pages_setup import CoursePageTestsFactory


class ModulePageTests(CoursePageTestsFactory):
    """Tests for Module Page - which should always redirect to parent course"""

    def testModuleRedirectsToCourse(self):
        Session.objects.all().delete()
        response = self.client.get("/academy/course/module-1/")
        self.assertRedirects(response, '/academy/course/', status_code=302, target_status_code=200, fetch_redirect_response=True)
