from django.contrib import admin
from materials.models import StudyMaterial

# Register your models here.


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "topic",
        "material_type",
        "is_published",
        "created_at",
    )

    list_filter = (
        "material_type",
        "is_published",
    )

    search_fields = (
        "title",
        "content",
        "topic__name",
    )