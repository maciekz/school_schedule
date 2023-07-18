import calendar

from rest_framework import fields, serializers

from schedule.models import ScheduleItem, StudentClass, Subject, Teacher


class QueryParamsSerializer(serializers.Serializer):
    """Serializer for query parameters."""

    for_today = fields.BooleanField(required=False)
    class_name = fields.CharField(required=False)


class StudentClassSummarySerializer(serializers.ModelSerializer):
    """Serializer for StudentClass summary."""

    student_count = serializers.SerializerMethodField()

    def get_student_count(self, obj):
        """Getter for student_count field"""
        return obj.students.count()

    class Meta:
        model = StudentClass
        fields = ["name", "student_count"]


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject."""

    class Meta:
        model = Subject
        fields = ["name"]


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher."""

    class Meta:
        model = Teacher
        fields = ["name"]


class ScheduleItemSerializer(serializers.ModelSerializer):
    """Serializer for ScheduleItem."""

    vars()["class"] = StudentClassSummarySerializer(source="student_class")
    day_of_week = serializers.SerializerMethodField()
    subject = SubjectSerializer()
    teacher = TeacherSerializer(source="subject.teacher")

    class Meta:
        model = ScheduleItem
        fields = ["class", "day_of_week", "hour", "subject", "teacher"]

    def get_day_of_week(self, obj):
        """Getter to display day_of_the_week name"""
        return calendar.day_name[obj.day_of_week]
