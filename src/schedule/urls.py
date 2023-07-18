"""schedule URL Configuration"""

from django.urls import path

from schedule import views

urlpatterns = [
    path("", views.ScheduleItemsListView.as_view(), name="schedule-items-list"),
]
