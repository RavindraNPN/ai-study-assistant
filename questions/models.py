from django.db import models
from academics.models import Topic


class Question(models.Model):

    QUESTION_TYPES = [
        ("pyq", "GTU PYQ"),
        ("mcq", "MCQ"),
        ("practice", "Practice"),
    ]

    DIFFICULTY_LEVELS = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES
    )

    question_text = models.TextField()

    marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default="medium"
    )

    answer = models.TextField(
        blank=True
    )

    explanation = models.TextField(
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="For GTU PYQ only"
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.question_text[:80]

class MCQOption(models.Model):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options"
    )

    option_text = models.CharField(
        max_length=500
    )

    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.option_text