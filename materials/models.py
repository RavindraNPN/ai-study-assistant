from django.db import models
from academics.models import Topic

# Create your models here.

class StudyMaterial(models.Model):

    MATERIAL_TYPES = [
        ("notes", "Notes"),
        ("pdf", "PDF"),
        ("revision", "Quick Revision"),
        ("example", "Example"),
    ]

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    title = models.CharField(max_length=255)

    material_type = models.CharField(
        max_length=20,
        choices=MATERIAL_TYPES,
        default="notes"
    )

    content = models.TextField(
        blank=True,
        help_text="Study material content"
    )

    pdf_file = models.FileField(
        upload_to="study_materials/",
        blank=True,
        null=True
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title