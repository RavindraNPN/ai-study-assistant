from django.db import models
from django.contrib.auth.models import User
from academics.models import Subject, Unit
from questions.models import Question


class MockTest(models.Model):

    title = models.CharField(max_length=255)

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="mock_tests"
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mock_tests"
    )

    duration_minutes = models.PositiveIntegerField(
        default=30
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class MockTestQuestion(models.Model):

    mock_test = models.ForeignKey(
        MockTest,
        on_delete=models.CASCADE,
        related_name="test_questions"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="mock_tests"
    )

    question_number = models.PositiveIntegerField()

    marks = models.PositiveIntegerField(
        default=1
    )

    class Meta:
        ordering = ["question_number"]
        unique_together = (
            "mock_test",
            "question_number"
        )

    def __str__(self):
        return f"{self.mock_test.title} - Q{self.question_number}"


class StudentAttempt(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="exam_attempts"
    )

    mock_test = models.ForeignKey(
        MockTest,
        on_delete=models.CASCADE,
        related_name="attempts"
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    score = models.PositiveIntegerField(
        default=0
    )

    is_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.student.username} - {self.mock_test.title}"


class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        StudentAttempt,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )

    selected_option = models.ForeignKey(
        "questions.MCQOption",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    text_answer = models.TextField(
        blank=True
    )

    is_correct = models.BooleanField(
        default=False
    )

    marks_obtained = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.attempt} - {self.question}"