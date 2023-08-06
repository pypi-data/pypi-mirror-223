"""LXP quiz specific Stream Blocks"""

from wagtail.blocks import (
    FieldBlock,
    StructBlock, IntegerBlock,
    DecimalBlock, BooleanBlock,
    RichTextBlock, ListBlock)


class MCAnswerBlock(StructBlock):
    text = RichTextBlock(required=True, help_text="Answer text")
    feedback = RichTextBlock(required=False, help_text="Feedback for this answer")
    fraction = DecimalBlock(required=True, label="Percent score", help_text="E.g. 1, 0.5, 0.33, 0")


class QuizItemBlock(StructBlock):
    """Generic quiz item block"""
    question_text = RichTextBlock(
        required=False,
        label="Question text"
    )
    shuffle_answers = BooleanBlock(
        default=False,
        required=False,
        label="Shuffle order of answers")
    default_mark = IntegerBlock(
        default=1,
        required=False,
        label="Default grade (max points)"
    )
    general_feedback = RichTextBlock(
        required=False,
        label="General Feedback after any answer"
    )
    correct_feedback = RichTextBlock(
        required=False,
        label="Correct Answer Feedback"
    )
    partially_correct_feedback = RichTextBlock(
        required=False,
        label="Partially Correct Answer Feedback"
    )
    incorrect_feedback = RichTextBlock(
        required=False,
        help_text="Incorrect Answer Feedback"
    )

    class Meta:
        abstract = True


class ItemTrueFalseBlock(QuizItemBlock):
    """True/False Quiz Item Block"""
    correct_answer = BooleanBlock(
        required=False,
        default=False,
        help_text="Select if TRUE is the correct answer. Leave unchecked for FALSE")

    class Meta:
        icon = 'cross'


class ItemMultiChoiceBlock(QuizItemBlock):
    """Multiple Choice Quiz Item Block"""
    single_choice = BooleanBlock(
        required=False,
        default=True,
        help_text="Uncheck to make the question multiple rather than single choice"
    )
    answers = ListBlock(MCAnswerBlock(required=True))

    class Meta:
        icon = 'list-ul'
