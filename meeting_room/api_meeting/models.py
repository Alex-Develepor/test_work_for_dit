from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MeetingRoom(models.Model):
    name = models.CharField(
        max_length=20
    )
    description = models.TextField()

    def __str__(self):

        return self.name


class ReservationRoom(models.Model):
    day = models.DateField()
    start_reservation = models.TimeField()
    end_reservation = models.TimeField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    meetingroom = models.ForeignKey(
        MeetingRoom,
        on_delete=models.CASCADE,
    )

    def is_occupied(self, current_time):
        return self.start_reservation <= current_time <= self.end_reservation


class LogForMeetingRoom(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    meetingroom = models.ForeignKey(
        MeetingRoom,
        on_delete=models.CASCADE,
    )
    period_reservation = models.CharField(max_length=50)
    informations = models.CharField(max_length=200)


