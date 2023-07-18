from datetime import time
from string import ascii_uppercase

import factory

POSSIBLE_STUDENT_CLASSES = [
    f"{number}{letter}" for number in range(1, 9) for letter in ascii_uppercase[:8]
]

POSSIBLE_SCHEDULE_HOURS = [time(hour=hour) for hour in range(8, 17)]

POSSIBLE_SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Computer Studies",
    "History",
    "English",
    "German",
    "Italian",
    "French",
    "Music",
    "Art",
    "Physical Education",
]


class StudentClassFactory(factory.django.DjangoModelFactory):
    """StudentClass factory."""

    name = factory.Faker("random_element", elements=POSSIBLE_STUDENT_CLASSES)

    class Meta:
        model = "schedule.StudentClass"


class StudentFactory(factory.django.DjangoModelFactory):
    """Student factory."""

    name = factory.Faker("name")
    student_class = factory.SubFactory(StudentClassFactory)

    class Meta:
        model = "schedule.Student"


class TeacherFactory(factory.django.DjangoModelFactory):
    """Teacher factory."""

    name = factory.Faker("name")

    class Meta:
        model = "schedule.Teacher"


class SubjectFactory(factory.django.DjangoModelFactory):
    """Subject factory."""

    name = factory.Faker("random_element", elements=POSSIBLE_SUBJECT_NAMES)
    teacher = factory.SubFactory(TeacherFactory)

    class Meta:
        model = "schedule.Subject"


class ScheduleItemFactory(factory.django.DjangoModelFactory):
    """ScheduleItem factory."""

    student_class = factory.SubFactory(StudentClassFactory)
    subject = factory.SubFactory(SubjectFactory)
    day_of_week = factory.Faker("random_element", elements=range(0, 5))
    hour = factory.Faker("random_element", elements=POSSIBLE_SCHEDULE_HOURS)

    class Meta:
        model = "schedule.ScheduleItem"
