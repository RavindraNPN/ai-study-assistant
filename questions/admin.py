from django.contrib import admin
from .models import Question, MCQOption


class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "question_text",
        "topic",
        "question_type",
        "difficulty",
        "marks",
        "year",
        "is_published",
    )

    list_filter = (
        "question_type",
        "difficulty",
        "year",
        "is_published",
    )

    search_fields = (
        "question_text",
        "answer",
        "explanation",
        "topic__name",
    )

    inlines = [
        MCQOptionInline
    ]


@admin.register(MCQOption)
class MCQOptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "option_text",
        "is_correct",
    )

    list_filter = (
        "is_correct",
    )