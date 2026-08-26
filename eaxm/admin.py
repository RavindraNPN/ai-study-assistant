from django.contrib import admin

from .models import (
    MockTest,
    MockTestQuestion,
    StudentAttempt,
    StudentAnswer,
)


class MockTestQuestionInline(admin.TabularInline):
    model = MockTestQuestion
    extra = 1


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "subject",
        "unit",
        "duration_minutes",
        "total_marks",
        "is_published",
    )

    list_filter = (
        "subject",
        "unit",
        "is_published",
    )

    search_fields = (
        "title",
    )

    inlines = [
        MockTestQuestionInline
    ]


@admin.register(MockTestQuestion)
class MockTestQuestionAdmin(admin.ModelAdmin):

    list_display = (
        "mock_test",
        "question_number",
        "question",
        "marks",
    )

    list_filter = (
        "mock_test",
    )


@admin.register(StudentAttempt)
class StudentAttemptAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "mock_test",
        "started_at",
        "submitted_at",
        "score",
        "is_completed",
    )

    list_filter = (
        "is_completed",
        "mock_test",
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "attempt",
        "question",
        "selected_option",
        "is_correct",
        "marks_obtained",
    )

    list_filter = (
        "is_correct",
    )