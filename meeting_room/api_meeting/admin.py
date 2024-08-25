from django.contrib import admin
from .models import MeetingRoom, ReservationRoom, LogForMeetingRoom

admin.site.register(MeetingRoom)
admin.site.register(ReservationRoom)
admin.site.register(LogForMeetingRoom)