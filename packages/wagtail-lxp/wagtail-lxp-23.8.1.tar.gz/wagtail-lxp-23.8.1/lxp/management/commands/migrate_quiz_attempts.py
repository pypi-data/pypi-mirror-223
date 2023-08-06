from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import models

from lxp.models import (
    QuizPage,
)
from lxp.models.quiz_attempt import QuizAttempt


class Command(BaseCommand):
    help = "Migrate quiz attempts, assuming courses, activities, and quizzes have already been migrated to target db."

    def add_arguments(self, parser):
        parser.add_argument("--fake", help="Perform a fake import, without any writes")

    def handle(self, *args, **options):
        # must have local postgresql database p1321_thrsp_old as db_old

        self.migrate_quiz_attempts()

    def migrate_quiz_attempts(self):
        # from db_old, get quiz slug + id

        self.stdout.write("")
        self.stdout.write("=========== QUIZ PAGES ===========")
        self.stdout.write("====================================")

        # quizzes = {}  # dict - holder for old-to-new quiz_id mapping
        query = f"""SELECT
                    s.page_ptr_id as id,
                    p.slug
                 from lxp_quizpage as s left join wagtailcore_page as p
                 on s.page_ptr_id = p.id"""

        for idx, m in enumerate(OldQuizShort.objects.raw(query).using("db_old")):
            new_quiz = QuizPage.objects.get(slug=m.slug)

            self.stdout.write(
                f"{idx}: Processing quiz {m.id}: ({m.slug}), new quiz id: {new_quiz.id}"
            )
            # quizzes[m.id] = {"slug": m.slug, "new_quiz_id": new_quiz.id}

            self.add_quiz_attempts(new_quiz, m.id)

        self.stdout.write("========= END QUIZ PAGES =========")
        self.stdout.write("====================================")

    def add_quiz_attempts(self, quiz_page, old_quiz_id):
        # from db_old, get all quiz attempt data
        query = f"""SELECT
                    id, user_id, quiz_id, created, answers, score
                    from lxp_quizattempt where quiz_id = {old_quiz_id}"""
        dots = ""
        for idx, m in enumerate(OldQuizAttempt.objects.raw(query).using("db_old")):
            dots += "."
            user = User.objects.get(id=m.user_id)
            qa = QuizAttempt.objects.create(
                quiz=quiz_page,
                user=user,
                score=m.score,
                answers=m.answers,
                created=m.created,
            )

            print(f"Added quiz {quiz_page.id} attempt for user {user.username}")


class OldQuizShort(models.Model):
    # Quiz model fields:
    id = models.IntegerField(primary_key=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        managed = False


class OldQuizAttempt(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    quiz_id = models.IntegerField()
    created = models.DateTimeField(blank=True, null=True)
    answers = models.JSONField(null=True)
    score = models.PositiveIntegerField(default=0)

    class Meta:
        managed = False


# class OldUserActivity(models.Model):
#     id = models.IntegerField(primary_key=True)
#     user_id = models.IntegerField()
#     activity_id = models.IntegerField()
#     created = models.DateTimeField(blank=True, null=True)
#     updated = models.DateTimeField(blank=True, null=True)
#     time_spent = models.PositiveIntegerField(default=0)
#     pct_score = models.PositiveIntegerField(default=0)
#     completed = models.BooleanField(default=False)
#     visits = models.PositiveIntegerField(default=0)

#     class Meta:
#         managed = False
