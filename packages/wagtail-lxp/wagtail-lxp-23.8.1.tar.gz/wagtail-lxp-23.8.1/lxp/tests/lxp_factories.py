import wagtail_factories
from lxp.models import AcademyPage, CoursePage, ModulePage, ActivityPage, QuizPage, SecurityOptions


class AcademyPageFactory(wagtail_factories.PageFactory):
    title = "Academy"

    class Meta:
        model = AcademyPage


class CoursePageFactory(wagtail_factories.PageFactory):
    title = "Course"
    summary = "Course A Summary"
    security = SecurityOptions.SECURITY_NONE

    class Meta:
        model = CoursePage


class SecureCoursePageFactory(wagtail_factories.PageFactory):
    title = "Secure Course"
    summary = "A Secure Course Summary"
    security = SecurityOptions.SECURITY_COURSE

    class Meta:
        model = CoursePage


class ModulePageFactory(wagtail_factories.PageFactory):
    title = "Module"

    class Meta:
        model = ModulePage


class ActivityPageFactory(wagtail_factories.PageFactory):
    title = "Activity"

    class Meta:
        model = ActivityPage


class QuizPageFactory(wagtail_factories.PageFactory):
    title = "Quiz"

    class Meta:
        model = QuizPage
