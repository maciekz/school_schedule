from calendar import weekday
from datetime import date

from rest_framework import generics

from schedule.models import ScheduleItem
from schedule.serializers import QueryParamsSerializer, ScheduleItemSerializer


class ScheduleItemsListView(generics.ListAPIView):
    pagination_class = None
    serializer_class = ScheduleItemSerializer

    def get_queryset(self):
        # Parameters
        params_serializer = QueryParamsSerializer(data=self.request.query_params)
        params_serializer.is_valid(raise_exception=True)

        queryset = ScheduleItem.objects.all()

        # Filtering
        class_name = params_serializer.validated_data.get("class_name")
        for_today = params_serializer.validated_data.get("for_today")
        if class_name:
            queryset = queryset.filter(student_class__name=class_name)
        if for_today:
            queryset = queryset.filter(day_of_week=date.today().weekday())

        # Optimisation
        queryset = queryset.select_related(
            "student_class", "subject", "subject__teacher"
        ).prefetch_related("student_class__students")

        return queryset.order_by("day_of_week", "hour")
