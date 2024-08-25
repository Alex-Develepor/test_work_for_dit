from datetime import datetime as dt

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import MeetingRoom, ReservationRoom
from .serializers import GetBookingSerializers


class MeetingRoomApiTest(APITestCase):

    def test_create_meeting_room(self):
        url = reverse('meetingroom-list')
        data = {'name': 'First room', 'description': 'test_info'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MeetingRoom.objects.count(), 1)
        self.assertEqual(MeetingRoom.objects.get().name, data['name'])


class ReservMeetingRoomApiTest(APITestCase):
    User.objects.create(
        email="user@example.com",
        username="test",
        password="123qweASD!"
    )

    MeetingRoom.objects.create(
        name='test room',
        description='test description'
    )

    def test_create_reserv(self):
        url = reverse('reservationmeetingroom-list')
        data = {
            "day": "2024-08-25",
            "start_reservation": "18:00",
            "end_reservation": "19:00",
            "user": 1,
            "meetingroom": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(ReservationRoom.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_equal_time_reserv(self):
        url = reverse('reservationmeetingroom-list')
        data = {
            "day": "2024-08-25",
            "start_reservation": "18:30",
            "end_reservation": "20:00",
            "user": 1,
            "meetingroom": 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(ReservationRoom.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_by_time(self):
        url = reverse('reservationmeetingroom-get_booking_today')
        data = {}
        response = self.client.get(url, data, format='json')
        result = []
        rooms = ReservationRoom.objects.filter(day=dt.today()).all()
        for room in rooms:
            serializer = GetBookingSerializers(room).data
            result.append(serializer)
        self.assertEqual(result, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)