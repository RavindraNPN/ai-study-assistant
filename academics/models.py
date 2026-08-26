from django.db import models

# Create your models here.

class Branch(models.Model):
    name =models.CharField(max_length=150)
    code=models.CharField( max_length=50,unique=True)

    def __str__(self):
        return self.name

class Semester(models.Model):
    branch=models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name="semesters"
    )
    number=models.PositiveIntegerField()

    class Meta:
        unique_together=("branch","number")
        ordering=['number']

    def __str__(self):
        return f"{self.branch.name} - Semester {self.number}"

class Subject(models.Model):
    semester=models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name= models.CharField(max_length=200)
    code= models.CharField(max_length=50)

    class Meta:
        unique_together=("semester","code")
    def __str__(self):
            return f"{self.code} - {self.name}"


class Unit(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="units"
    )
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=200)

    class Meta:
        unique_together = ("subject", "number")
        ordering = ["number"]

    def __str__(self):
        return f"Unit {self.number} - {self.name}"


class Topic(models.Model):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name="topics"
    )
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name
