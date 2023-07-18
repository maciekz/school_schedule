import calendar

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class StudentClass(models.Model):
    """Model representing a class."""

    name = models.CharField(db_index=True)

    def __str__(self):
        return f"{self.name}"


class Student(models.Model):
    """Model representing a student."""

    name = models.CharField()
    student_class = models.ForeignKey(
        StudentClass, null=True, on_delete=models.SET_NULL, related_name="students"
    )

    def __str__(self):
        return f"{self.name}, StudentClass: {self.student_class}"


class Teacher(models.Model):
    """Model representing a teacher."""

    name = models.CharField()

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    """Model representing a subject."""

    name = models.CharField()
    teacher = models.ForeignKey(
        Teacher, null=True, on_delete=models.SET_NULL, related_name="subjects"
    )

    def __str__(self):
        return f"{self.name}, Teacher: {self.teacher}"


class ScheduleItem(models.Model):
    """Model representing a schedule item."""

    student_class = models.ForeignKey(
        StudentClass,
        null=True,
        on_delete=models.SET_NULL,
        related_name="schedule_items",
    )
    subject = models.ForeignKey(
        Subject, null=True, on_delete=models.SET_NULL, related_name="schedule_items"
    )
    day_of_week = models.IntegerField(
        db_index=True, validators=[MinValueValidator(0), MaxValueValidator(6)]
    )
    hour = models.TimeField()

    def __str__(self):
        name_of_day = calendar.day_name[self.day_of_week]
        return (
            f"StudentClass: {self.student_class}, Day of week: {name_of_day}, "
            f"Hour: {self.hour}, Subject: {self.subject}"
        )
