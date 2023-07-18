from datetime import date
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status

from schedule import factories

pytestmark = pytest.mark.django_db


MONDAY = date(year=2023, month=7, day=17)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def schedule_items():
    class_1a = factories.StudentClassFactory(name="1A")
    factories.StudentFactory.create_batch(25, student_class=class_1a)
    # Monday lessons
    factories.ScheduleItemFactory.create_batch(5, student_class=class_1a, day_of_week=0)
    # Thursday lessons
    factories.ScheduleItemFactory.create_batch(8, student_class=class_1a, day_of_week=3)

    class_5b = factories.StudentClassFactory(name="5B")
    factories.StudentFactory.create_batch(31, student_class=class_5b)
    # Monday lessons
    factories.ScheduleItemFactory.create_batch(7, student_class=class_5b, day_of_week=0)
    # Friday lessons
    factories.ScheduleItemFactory.create_batch(3, student_class=class_5b, day_of_week=3)
    yield


class TestScheduleItemsListView:
    url = reverse("schedule-items-list")

    def test_empty_schedule(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_all_schedule_items(self, api_client, schedule_items):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 23

    @pytest.mark.parametrize(
        "class_name, schedule_items_count", [("1A", 13), ("5B", 10), ("8C", 0)]
    )
    def test_all_schedule_items_for_class(
        self, class_name, schedule_items_count, api_client, schedule_items
    ):
        response = api_client.get(self.url, data={"class_name": class_name})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == schedule_items_count

    @pytest.mark.parametrize(
        "for_today, schedule_items_count", [("true", 12), ("false", 23)]
    )
    def test_schedule_items_for_today(
        self, for_today, schedule_items_count, api_client, schedule_items
    ):
        with patch("schedule.views.date") as mock_date:
            mock_date.today.return_value = MONDAY

            response = api_client.get(self.url, data={"for_today": for_today})
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()) == schedule_items_count

    @pytest.mark.parametrize(
        "class_name, for_today, schedule_items_count",
        [
            ("1A", "true", 5),
            ("1A", "false", 13),
            ("5B", "true", 7),
            ("5B", "false", 10),
            ("8C", "true", 0),
            ("8C", "false", 0),
        ],
    )
    def test_schedule_items_for_today_for_class(
        self,
        class_name,
        for_today,
        schedule_items_count,
        api_client,
        schedule_items,
    ):
        with patch("schedule.views.date") as mock_date:
            mock_date.today.return_value = MONDAY

            response = api_client.get(
                self.url, data={"class_name": class_name, "for_today": for_today}
            )
            assert response.status_code == status.HTTP_200_OK
            assert len(response.json()) == schedule_items_count
