from datetime import time

import pytest

from schedule import factories, serializers

pytestmark = pytest.mark.django_db


@pytest.fixture
def student_class_empty():
    return factories.StudentClassFactory()


@pytest.fixture
def student_class(student_class_empty):
    factories.StudentFactory.create_batch(5, student_class=student_class_empty)
    return student_class_empty


@pytest.fixture
def teacher():
    return factories.TeacherFactory()


@pytest.fixture
def subject(teacher):
    return factories.SubjectFactory(teacher=teacher)


@pytest.fixture
def schedule_item(student_class, subject):
    return factories.ScheduleItemFactory(
        student_class=student_class,
        subject=subject,
        day_of_week=0,
        hour=time(hour=8, minute=30),
    )


def test_student_class_summary_serializer_empty(student_class_empty):
    expected = {"name": student_class_empty.name, "student_count": 0}

    assert (
        serializers.StudentClassSummarySerializer(student_class_empty).data == expected
    )


def test_student_class_summary_serializer(student_class):
    expected = {"name": student_class.name, "student_count": 5}

    assert serializers.StudentClassSummarySerializer(student_class).data == expected


def test_subject_serializer(subject):
    expected = {"name": subject.name}

    assert serializers.SubjectSerializer(subject).data == expected


def test_teacher_serializer(teacher):
    expected = {"name": teacher.name}

    assert serializers.TeacherSerializer(teacher).data == expected


def test_schedule_item_serializer(schedule_item, student_class, subject, teacher):
    expected = {
        "class": {"name": student_class.name, "student_count": 5},
        "subject": {"name": subject.name},
        "day_of_week": "Monday",
        "hour": "08:30:00",
        "teacher": {"name": teacher.name},
    }

    assert serializers.ScheduleItemSerializer(schedule_item).data == expected
