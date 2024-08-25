from django.contrib import admin

from .models import LogForMeetingRoom, MeetingRoom, ReservationRoom

admin.site.register(MeetingRoom)
admin.site.register(ReservationRoom)
admin.site.register(LogForMeetingRoom)