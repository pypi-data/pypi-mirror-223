import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from wagtail.fields import RichTextField
from wagtail.models import Page

from lxp.models import (
    AcademyPage,
    ActivityPage,
    CoursePage,
    ModulePage,
    QuizPage,
    Topic,
    UserActivity,
)
from lxp.models.activity import ActivityPageRelatedAuthor, ActivityPageRelatedLink
from lxp.models.security import EnrollmentOptions, SecurityOptions


class Command(BaseCommand):
    help = "Migrate non-cms courses (from external db) into cms-based courses."

    parent_id = 3
    # fake = False
    skip_modules = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--parent_id",
            help="Parent page id (above academy). If none, will use default.",
        )

        parser.add_argument(
            "--skip_modules", help="Skip importing modules and activities."
        )

        # parser.add_argument(
        #     '--fake',
        #     help='Perform a fake import, only read & transform stages')

    def handle(self, *args, **options):
        # must have local postgresql database p1321_thrsp_old as db_old

        if options["parent_id"]:
            self.parent_id = int(options["parent_id"])

        if Page.objects.filter(id=self.parent_id).count() == 0:
            raise CommandError(f"Parent page id ({self.parent_id}) not found. Exiting.")

        if options["skip_modules"]:
            self.skip_modules = options["skip_modules"] in ["True", "true", "1"]

        # if options['fake']:
        #     self.fake = options['fake'] in ['True', 'true', '1']
        #     self.stdout.write("Fake mode active")

        print("Starting migration...")

        self.migrate_academies()

    def migrate_academies(self):
        # get academy from db_old,
        # if new db does not have an academy with the same name and slug, create it

        self.stdout.write("")
        self.stdout.write("====================================")
        self.stdout.write("========== ACADEMY PAGES ===========")
        self.stdout.write("====================================")

        parent_page = Page.objects.get(id=self.parent_id)

        for idx, m in enumerate(
            OldAcademy.objects.raw(
                """SELECT 
                    s.page_ptr_id,
                    p.path,
                    p.title,
                    p.slug,
                    p.live,
                    s.description,
                    s.instruction_text,
                    s.instruction_file_id
                 from lxp_academypage as s left join wagtailcore_page as p 
                 on s.page_ptr_id = p.id"""
            ).using("db_old")
        ):
            self.stdout.write("")
            self.stdout.write(
                f"{idx}: Processing Academy page {m.page_ptr_id}: ({m.slug})"
            )

            # if page with a given slug exists, just read it
            try:
                p = AcademyPage.objects.child_of(parent_page).get(
                    slug=m.slug, title=m.title
                )
                created = False
                self.stdout.write(f"-- Found existing Academy Page {p.slug}")
            except AcademyPage.DoesNotExist:
                p = AcademyPage(
                    slug=m.slug,
                    title=m.title,
                    live=m.live,
                    description=m.description,
                    instruction_text=m.instruction_text,
                    instruction_file_id=m.instruction_file_id,
                )
                created = True
                self.stdout.write(f"----- Created Academy Page {p.slug}")
            if created:
                parent_page.add_child(instance=p)
            p.save()

            # migrate all courses for this academy
            self.migrate_courses(p, m.path)

    def migrate_courses(self, parent_page, old_parent_path):
        # get course from db_old,
        # if new db does not have a course with the same name and slug,
        # create it

        self.stdout.write("")
        self.stdout.write("=========== COURSE PAGES ===========")
        self.stdout.write("====================================")

        path_len = len(old_parent_path)
        query = f"""SELECT
                    s.page_ptr_id,
                    p.path,
                    p.title,
                    p.slug,
                    p.live,
                    s.description,
                    s.summary,
                    s.enrollment,
                    s.security,
                    s.course_image_id
                 from lxp_coursepage as s left join wagtailcore_page as p
                 on s.page_ptr_id = p.id
                 where substring(p.path from 1 for {path_len}) = '{old_parent_path}' """

        for idx, m in enumerate(OldCourse.objects.raw(query).using("db_old")):
            self.stdout.write(f"{idx}: Processing course {m.page_ptr_id}: ({m.slug})")
            # if a course page with a given slug exists, just read it
            try:
                p = CoursePage.objects.child_of(parent_page).get(
                    slug=m.slug, title=m.title
                )
                created = False
                self.stdout.write(f"-- Found existing Course Page {p.slug}")
            except CoursePage.DoesNotExist:
                p = CoursePage(
                    slug=m.slug,
                    title=m.title,
                    live=m.live,
                    summary=m.summary,
                    description=m.description,
                    enrollment=m.enrollment,
                    security=m.security,
                    cover_image_id=m.course_image_id,
                )
                created = True
                self.stdout.write(f"---- Created Course Page {p.slug}")
            if created:
                parent_page.add_child(instance=p)
                p.save()

            # update linked course topics
            query = f"SELECT id, coursepage_id, topic_id from lxp_coursepage_topics where coursepage_id = {m.page_ptr_id}"
            for j, old in enumerate(OldCourseTopic.objects.raw(query).using("db_old")):
                t = Topic.objects.get(id=old.topic_id)
                p.topics.add(t)
                p.save()
                self.stdout.write(f"---- Added topic {t.slug} to course {p.slug}")

            if not self.skip_modules:
                self.migrate_modules(p, m.path)

        self.stdout.write("========= END COURSE PAGES =========")
        self.stdout.write("====================================")

    def migrate_modules(self, parent_page, old_parent_path):
        # get modules from db_old,
        # if new db does not have a module with the same name and slug,
        # create it

        self.stdout.write("")
        self.stdout.write("=========== MODULE PAGES ===========")
        self.stdout.write("====================================")

        path_len = len(old_parent_path)
        query = f"""SELECT
                    s.page_ptr_id,
                    p.path,
                    p.title,
                    p.slug,
                    p.live,
                    s.description,
                    s.summary,
                    s.module_image_id
                 from lxp_modulepage as s left join wagtailcore_page as p
                 on s.page_ptr_id = p.id
                 where substring(p.path from 1 for {path_len}) = '{old_parent_path}' """

        for idx, m in enumerate(OldModule.objects.raw(query).using("db_old")):
            self.stdout.write(f"{idx}: Processing module {m.page_ptr_id}: ({m.slug})")
            # if a module page with a given slug exists, just read it
            try:
                p = ModulePage.objects.child_of(parent_page).get(
                    slug=m.slug, title=m.title
                )
                created = False
                self.stdout.write(f"-- Found existing Module Page {p.slug}")
            except ModulePage.DoesNotExist:
                p = ModulePage(
                    slug=m.slug,
                    title=m.title,
                    live=m.live,
                    summary=m.summary,
                    description=m.description,
                    cover_image_id=m.module_image_id,
                )
                created = True
                self.stdout.write(f"--- Created Module Page {p.slug}")
            if created:
                parent_page.add_child(instance=p)
            p.save()

            self.migrate_activities(p, m.path)
            self.migrate_quizzes(p, m.path)

        self.stdout.write("========= END MODULE PAGES =========")
        self.stdout.write("====================================")

    def migrate_activities(self, parent_page, old_parent_path):
        # get activities from db_old,
        # if new db does not have an activity with the same name and slug under given parent,
        # create it

        self.stdout.write("")
        self.stdout.write("=========== ACTIVITY PAGES ===========")
        self.stdout.write("====================================")

        path_len = len(old_parent_path)
        query = f"""SELECT
                    s.page_ptr_id,
                    p.path,
                    p.title,
                    p.slug,
                    p.live,
                    s.summary,
                    s.icon,
                    s.publication_year,
                    s.content,
                    s.content_length
                 from lxp_activitypage as s left join wagtailcore_page as p
                 on s.page_ptr_id = p.id
                 where substring(p.path from 1 for {path_len}) = '{old_parent_path}' """

        for idx, m in enumerate(OldActivity.objects.raw(query).using("db_old")):
            self.stdout.write(f"{idx}: Processing activity {m.page_ptr_id}: ({m.slug})")
            # if an activity page with a given slug exists, just read it
            try:
                p = ActivityPage.objects.child_of(parent_page).get(
                    slug=m.slug, title=m.title
                )
                created = False
                self.stdout.write(f"-- Found existing Activity Page {p.slug}")
            except ActivityPage.DoesNotExist:
                p = ActivityPage(
                    slug=m.slug,
                    title=m.title,
                    live=m.live,
                    summary=m.summary,
                    icon=m.icon,
                    publication_year=m.publication_year,
                    content=m.content,
                    content_length=m.content_length,
                )
                created = True
                self.stdout.write(f"-- Created Activity Page {p.slug}")
            if created:
                parent_page.add_child(instance=p)
            p.save()

            # update activityPageRelatedLinks
            self.update_related_links(p, m.page_ptr_id)
            self.update_related_authors(p, m.page_ptr_id)

            # update userActivity
            self.update_user_activity(p, m.page_ptr_id)

        self.stdout.write("========= END ACTIVITY PAGES =========")
        self.stdout.write("====================================")

    def migrate_quizzes(self, parent_page, old_parent_path):
        # get quizzes from db_old,
        # if new db does not have a quiz with the same name and slug under given parent,
        # create it

        self.stdout.write("")
        self.stdout.write("=========== QUIZ PAGES ===========")
        self.stdout.write("====================================")

        path_len = len(old_parent_path)
        query = f"""SELECT
                    s.page_ptr_id,
                    p.path,
                    p.title,
                    p.slug,
                    p.live,
                    s.summary,
                    s.description,
                    s.content,
                    s.attempts_allowed,
                    s.minutes_between_attempts,
                    s.score_to_complete
                 from lxp_quizpage as s left join wagtailcore_page as p
                 on s.page_ptr_id = p.id
                 where substring(p.path from 1 for {path_len}) = '{old_parent_path}' """

        for idx, m in enumerate(OldQuiz.objects.raw(query).using("db_old")):
            self.stdout.write(f"{idx}: Processing quiz {m.page_ptr_id}: ({m.slug})")
            # if a quiz page with a given slug exists, just read it
            try:
                p = QuizPage.objects.child_of(parent_page).get(
                    slug=m.slug, title=m.title
                )
                created = False
                self.stdout.write(f"-- Found existing Quiz Page {p.slug}")
            except QuizPage.DoesNotExist:
                p = QuizPage(
                    slug=m.slug,
                    title=m.title,
                    live=m.live,
                    summary=m.summary,
                    description=m.description,
                    content=m.content,
                    attempts_allowed=m.attempts_allowed,
                    minutes_between_attempts=m.minutes_between_attempts,
                    score_to_complete=m.score_to_complete,
                )
                created = True
                self.stdout.write(f"-- Created Quiz Page {p.slug}")
            if created:
                parent_page.add_child(instance=p)
            p.save()

        self.stdout.write("========= END QUIZ PAGES =========")
        self.stdout.write("====================================")

    def update_related_links(self, page, old_page_ptr_id):
        # get related links from db_old,
        query = f"""SELECT
                    id, page_id, sort_order, name, url
                    from lxp_activitypagerelatedlink
                    where page_id = {old_page_ptr_id}"""

        for idx, m in enumerate(OldRelatedLink.objects.raw(query).using("db_old")):
            self.stdout.write(
                f"\n-- Processing rel-link {m.id} for activity_page {m.page_id}: {m.name}"
            )

            if ActivityPageRelatedLink.objects.filter(
                page=page, name=m.name, url=m.url
            ).exists():
                self.stdout.write(
                    f"-- Found existing rel-link {m.name} for activity_page {m.page_id}"
                )
                continue

            rl = ActivityPageRelatedLink(
                page=page, name=m.name, url=m.url, sort_order=m.sort_order
            )
            rl.save()

    def update_related_authors(self, page, old_page_ptr_id):
        # get related authors from db_old,
        query = f"""SELECT
                    id, page_id, sort_order, name, country, affiliation
                    from lxp_activitypagerelatedauthor
                    where page_id = {old_page_ptr_id}"""

        for idx, m in enumerate(OldRelatedAuthor.objects.raw(query).using("db_old")):
            self.stdout.write(
                f"\n-- Processing rel-author {m.id} for activity_page {m.page_id}: {m.name}"
            )

            if ActivityPageRelatedAuthor.objects.filter(
                page=page, name=m.name, country=m.country
            ).exists():
                self.stdout.write(
                    f"-- Found existing rel-author {m.name} for activity_page {m.page_id}"
                )
                continue

            ra = ActivityPageRelatedAuthor(
                page=page,
                name=m.name,
                country=m.country,
                affiliation=m.affiliation,
                sort_order=m.sort_order,
            )
            ra.save()

    def update_user_activity(self, page, old_page_ptr_id):
        query = f"""SELECT
                    id, user_id, activity_id, created, updated, time_spent, pct_score, completed, visits
                    from lxp_useractivity where activity_id = {old_page_ptr_id}"""
        self.stdout.write(f"\n-- User_activity for {old_page_ptr_id}: ")
        dots = ""
        for idx, m in enumerate(OldUserActivity.objects.raw(query).using("db_old")):
            dots += "."
            try:
                ua = UserActivity.objects.get(activity_id=page.id, user_id=m.user_id)
            except UserActivity.DoesNotExist:
                user = User.objects.get(id=m.user_id)
                page.users.add(
                    user,
                    through_defaults={
                        "created": m.created,
                        "updated": m.updated,
                        "time_spent": m.time_spent,
                        "pct_score": m.pct_score,
                        "completed": m.completed,
                        "visits": m.visits,
                    },
                )
                page.save()

        self.stdout.write(f"{dots}\n")


class OldAcademy(models.Model):
    """Temp holder for old academy data"""

    page_ptr_id = models.IntegerField(primary_key=True)
    path = (models.CharField(max_length=255),)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    live = models.BooleanField(default=True)
    description = RichTextField(null=True, blank=True)
    instruction_text = RichTextField(null=True, blank=True)
    instruction_file_id = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    list_visible = models.BooleanField(default=True, help_text="Show list of courses")

    class Meta:
        managed = False


class OldCourse(models.Model):
    """Temp holder for old course data"""

    page_ptr_id = models.IntegerField(primary_key=True)
    path = (models.CharField(max_length=255),)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    live = models.BooleanField(default=True)
    summary = RichTextField(blank=True, help_text="Brief summary for the overview page")
    description = RichTextField(
        blank=True, help_text="Full description for course Index Page"
    )
    enrollment = models.IntegerField(
        choices=EnrollmentOptions.choices, default=EnrollmentOptions.ENROLL_AUTOMATIC
    )
    security = models.IntegerField(
        choices=SecurityOptions.choices, default=SecurityOptions.SECURITY_NONE
    )
    course_image_id = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False


class OldModule(models.Model):
    """Temp holder for old module data"""

    page_ptr_id = models.IntegerField(primary_key=True)
    path = (models.CharField(max_length=255),)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    live = models.BooleanField(default=True)
    summary = RichTextField(blank=True, help_text="Brief summary for the overview page")
    description = RichTextField(
        blank=True, help_text="Full description for Module Index Page"
    )
    module_image_id = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False


class OldActivity(models.Model):
    page_ptr_id = models.IntegerField(primary_key=True)
    path = (models.CharField(max_length=255),)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    live = models.BooleanField(default=True)
    summary = RichTextField(null=True, blank=True)
    icon = models.CharField(max_length=32, null=True, blank=True)
    publication_year = models.IntegerField(
        null=True, blank=True, default=datetime.datetime.now().year
    )
    content = models.TextField(null=True, blank=True)
    content_length = models.IntegerField(null=True, blank=True)

    # many-to-many:
    # users = models.ManyToManyField("auth.User", through="UserActivity")
    # related_links
    # related_authors

    class Meta:
        managed = False


class OldQuiz(models.Model):
    # Quiz model fields:
    page_ptr_id = models.IntegerField(primary_key=True)
    path = (models.CharField(max_length=255),)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    live = models.BooleanField(default=True)
    summary = RichTextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    attempts_allowed = models.PositiveIntegerField(null=True, blank=True)
    minutes_between_attempts = models.PositiveIntegerField(null=True, blank=True)
    score_to_complete = models.PositiveIntegerField(null=True, blank=True)

    # many-to-many with users (for tracking quiz attempts).
    # Allow multiple user-quiz pairs (no user-quiz unique constraint)
    # users = models.ManyToManyField('auth.User', through='QuizAttempt')

    class Meta:
        managed = False


class OldCourseTopic(models.Model):
    id = models.IntegerField(primary_key=True)
    coursepage_id = models.IntegerField()
    topic_id = models.IntegerField()

    class Meta:
        managed = False


class OldRelatedLink(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField()
    sort_order = models.IntegerField()
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=1024)

    class Meta:
        managed = False


class OldRelatedAuthor(models.Model):
    id = models.IntegerField(primary_key=True)
    page_id = models.IntegerField()
    sort_order = models.IntegerField()
    name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    affiliation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False


class OldUserActivity(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    activity_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    time_spent = models.PositiveIntegerField(default=0)
    pct_score = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    visits = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False
