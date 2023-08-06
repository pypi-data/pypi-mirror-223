from django.utils.html import format_html_join
from django.templatetags.static import static

from django.urls import path, re_path, reverse
from wagtail import hooks
from wagtail.admin import widgets as wagtailadmin_widgets
from lxp.models.quiz import QuizPage
from wagtail.contrib.modeladmin.options import modeladmin_register

from .models.admin_sidebar import AcademyAdmin
from .views import quiz_summary


@hooks.register("insert_editor_js")
def editor_js():
    # @TODO: this is executed for any page type, how to make it executed only for specific models?
    js_files = [
        "lxp/js/activity_editor.js",  # https://fireworks.js.org
    ]
    return format_html_join(
        "\n",
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )


@hooks.register("register_admin_urls")
def register_quiz_summary_url():
    return [
        path("quiz/summary/<int:pk>/", quiz_summary, name="quiz_summary"),
    ]


@hooks.register("register_page_listing_buttons")
def page_listing_buttons(page, page_perms, is_parent=False, next_url=None):
    # if page is of type QuizPage, exit
    if page.get_verbose_name() == QuizPage.get_verbose_name():
        wagtail_admin_home_url = reverse("wagtailadmin_home")
        yield wagtailadmin_widgets.PageListingButton(
            "Results", f"{wagtail_admin_home_url}quiz/summary/{page.pk}/", priority=10
        )

modeladmin_register(AcademyAdmin)