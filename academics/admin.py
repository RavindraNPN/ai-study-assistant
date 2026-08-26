from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("branch", "number")
    list_filter = ("branch",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "semester")
    list_filter = ("semester",)
    search_fields = ("name", "code")


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "subject")
    list_filter = ("subject",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "unit")
    list_filter = ("unit",)
    search_fields = ("name",)