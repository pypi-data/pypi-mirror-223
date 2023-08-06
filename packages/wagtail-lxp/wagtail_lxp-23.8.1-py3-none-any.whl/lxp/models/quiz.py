from decimal import Decimal
from math import ceil

from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
)
from wagtail import blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

import lxp.models
from ..blocks_quiz import ItemMultiChoiceBlock, ItemTrueFalseBlock


class QuizPage(Page):
    """Quiz in a Module in LXP system"""

    FALSE_CODE = 1  # for TF items
    TRUE_CODE = 2  # for TF items

    parent_page_types = ["lxp.ModulePage"]
    subpage_types = []

    template = "lxp/pages/quiz_page.html"

    # Quiz model fields:
    summary = RichTextField(
        null=True,
        blank=True,
        help_text="Brief quiz summary for the list of activities page",
    )

    description = RichTextField(
        null=True,
        blank=True,
        help_text="Optional instruction for the quiz. If not defined, summary will be used.",
    )

    content = StreamField(
        [
            ("item_truefalse", ItemTrueFalseBlock()),
            ("item_multichoice", ItemMultiChoiceBlock()),
            ("rich_text", blocks.RichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
            ("embedded_video", EmbedBlock(icon="media")),
        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    attempts_allowed = models.PositiveIntegerField(
        default=999999, help_text="Max number of attempts allowed"
    )
    minutes_between_attempts = models.PositiveIntegerField(
        default=0, help_text="Time gap between consecutive attempts, 0=none"
    )
    score_to_complete = models.PositiveIntegerField(
        default=1,
        help_text="Minimum percent score to consider the quiz completed: "
        "0 - none, 1 - 1%, 100 - 100%",
    )

    # many-to-many with users (for tracking quiz attempts).
    # Allow multiple user-quiz pairs (no user-quiz unique constraint)
    users = models.ManyToManyField("auth.User", through="QuizAttempt")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("summary"),
                FieldPanel("description"),
            ],
            heading="Summary (for List of Activities page) "
            "and optional description (for Quiz page)",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                FieldPanel("score_to_complete"),
                FieldPanel("attempts_allowed"),
                FieldPanel("minutes_between_attempts"),
            ],
            heading="Limits on repeated attempts",
            classname="collapsible",
        ),
        FieldPanel("content"),
    ]

    @property
    def course_page(self):
        return self.get_ancestors().type(lxp.models.CoursePage).last().specific

    @property
    def module_page(self):
        return self.get_parent().specific

    def mark_content_items(self):
        """adds is_item and index properties to each content element
        for easy processing of items vs non-items"""
        counter = 0
        for element in self.content:
            element.is_item = bool(element.block_type.startswith("item_"))
            if element.is_item:
                counter += 1
            element.index = counter if element.is_item else 0
        return counter

    def get_content_items(self):
        """returns a list of content items (non-items are ignored)"""
        return [element for element in self.content if element.is_item]

    def get_context(self, request, *args, **kwargs):
        context = super(QuizPage, self).get_context(request, *args, **kwargs)
        context["course_page"] = self.course_page
        context["module_page"] = self.module_page

        course_modules = self.course_page.get_modules()
        context["modules"] = course_modules

        context["num_items"] = self.mark_content_items()
        context["tf_answers"] = {
            self.FALSE_CODE: "False",
            self.TRUE_CODE: "True",
        }  # only used in TF items
        context["quiz"] = self
        return context

    def get_attempts_for_user(self, user_id):
        """Return user attempts at quiz"""
        return lxp.models.QuizAttempt.objects.filter(quiz_id=self.id, user_id=user_id)

    def get_attempts(self):
        """Return all attempts at given quiz"""
        return lxp.models.QuizAttempt.objects.filter(quiz_id=self.id)

    # def get_num_attempts(self, user_id):
    #     qa = self.get_attempts(user_id).aggregate(Count('score'))

    # def calculate_score(self, user_answers):
    #     """given a json object with key/val pairs of item-uuid: answer to item,
    #     return a percent score."""
    #     #TODO: is this used at all?
    #     self.mark_content_items()
    #
    #     # create a dict of correct answers {ans_code, fraction}, to compare with actual answers
    #     correct_answers = {}
    #
    #     for element in filter(lambda e: e.block_type.startswith("item_"), self.content):
    #
    #         # TF item
    #         if element.block_type == "item_truefalse":
    #             code = (
    #                 self.TRUE_CODE
    #                 if element.value["correct_answer"] is True
    #                 else self.FALSE_CODE
    #             )
    #
    #             correct_answers[element.id] = code
    #
    #         # MC item
    #         if element.block_type == "item_multichoice":  # 1-A, 2-B...
    #             for idx, val in enumerate(element.value["answers"], start=1):
    #                 fraction = Decimal(val["fraction"].strip(' "'))
    #                 if (
    #                     fraction == 1
    #                 ):  # TODO: add support for partial fractions
    #                     correct_answers[element.id] = idx
    #
    #     # intersecting two dictionaries: users_answers present in correct_answers
    #     valid_user_answers = {
    #         x: user_answers[x]
    #         for x in user_answers
    #         if x in correct_answers and user_answers[x] == correct_answers[x]
    #     }
    #
    #     final_score = int((len(valid_user_answers) * 100) / len(correct_answers))
    #     return final_score

    def calculate_score(self, user_answers):
        """
        Given a json object with key/val pairs of item-uuid: answer to item,
        return a percent score.
        """
        # TODO: is this used at all?
        self.mark_content_items()

        # create a dict of correct answers {ans_code, fraction}, to compare with actual answers
        scored_user_answers = {}

        content_items = self.get_content_items()

        for element in content_items:

            eltid = element.id

            if eltid not in user_answers:
                scored_user_answers[eltid] = 0
                continue

            # TF item
            if element.block_type == "item_truefalse":
                scored_user_answers[eltid] = self.evaluate_item_truefalse(
                    element, user_answers[eltid]
                )
                continue
            # MC item
            if element.block_type == "item_multichoice":  # 1-A, 2-B...
                scored_user_answers[eltid] = self.evaluate_item_multichoice(
                    element, user_answers[eltid]
                )
                continue

        final_score = int(sum(scored_user_answers.values()) / len(content_items))
        print(final_score)
        return final_score

    def evaluate_item_truefalse(self, item, user_answer):
        """There are no fractional points in T/F items, so return either 0 or 100%"""
        correct_answer = (
            self.TRUE_CODE if item.value["correct_answer"] is True else self.FALSE_CODE
        )
        return 100 if user_answer == correct_answer else 0

    def evaluate_item_multichoice(self, item, user_answer):
        for idx, val in enumerate(item.value["answers"], start=1):
            if user_answer == idx:
                fraction = (
                    val["fraction"]
                    if isinstance(val["fraction"], Decimal)
                    else Decimal(val["fraction"].strip(' "'))
                )

                return int(fraction * 100)
        return 0

    def get_distribution_of_answers(self):
        """returns a 2d dictionary answer_counts[item_id][answer_code] = count"""
        answer_counts = {}

        # initialize answer_counts with item ids and answer codes in proper order
        items = self.get_content_items()
        for item in items:
            answer_counts[item.id] = {}
            if item.block_type == "item_truefalse":
                answer_counts[item.id][self.FALSE_CODE] = 0
                answer_counts[item.id][self.TRUE_CODE] = 0
            elif item.block_type == "item_multichoice":
                for idx, val in enumerate(item.value["answers"], start=1):
                    answer_counts[item.id][idx] = 0

        attempts = self.get_attempts()
        for user_attempt in attempts:  # for each attempt (in all items)
            user_answers = user_attempt.answers
            for item_id, answer in user_answers.items():
                if item_id not in answer_counts:
                    answer_counts[item_id] = {}
                if answer not in answer_counts[item_id]:
                    answer_counts[item_id][answer] = 0
                answer_counts[item_id][answer] += 1
        return answer_counts

    def get_score_bins(self, limit_to_best=False):
        """returns an array [0..9] with 10 bins, with score counts in each bin.
        If limit_to_best is True, only the best score for each user/session_key is returned."""

        score_counts = [0] * 10  # initialize with 10 bins

        if limit_to_best:
            scores = (
                lxp.models.QuizAttempt.objects.filter(quiz_id=self.id)
                .order_by("session_key", "-score")
                .distinct("session_key")
                .values_list("score", flat=True)
            )
        else:
            scores = lxp.models.QuizAttempt.objects.filter(quiz_id=self.id).values_list(
                "score", flat=True
            )

        for score in scores:
            score_counts[ceil(max(1, score) / 10) - 1] += 1

        return score_counts

    # AJAX Submit is processed in the view.
