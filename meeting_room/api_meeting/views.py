from datetime import datetime as dt
from http import HTTPStatus

from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .create_report import create_report
from .models import LogForMeetingRoom, MeetingRoom, ReservationRoom, User
from .serializers import (CreateReservationRoomSerializer,
                          GetBookingSerializers, GetReservationRoomSerializer,
                          LogSerializer, MeetingRoomSerializer)


class MeetingRoomView(viewsets.ModelViewSet):
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer


class ReservationMeetingRoomView(viewsets.ModelViewSet):
    queryset = ReservationRoom.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GetReservationRoomSerializer
        elif self.action == 'get_booking':
            return GetBookingSerializers
        else:
            return CreateReservationRoomSerializer

    @swagger_auto_schema()
    @action(detail=False, methods=('get',), url_path='get_booking', url_name='get_booking')
    def get_booking_today(self, request, *args, **kwargs):
        print(request.data)
        try:
            day = request.data['day']
        except KeyError:
            day = dt.today().date()
        try:
            time = request.data['time']
        except KeyError:
            time = None
        try:
            meting_room = request.data['meetingroom']
        except KeyError:
            meting_room = None
        if meting_room is None:
            rooms = ReservationRoom.objects.filter(day=day).all()
        else:
            rooms = ReservationRoom.objects.filter(day=day, meetingroom=MeetingRoom.objects.get(id=meting_room)).all()
        result = []
        for room in rooms:
            serializer = self.get_serializer(room).data
            if time is not None:
                if room.is_occupied(dt.strptime(time, '%H:%M').time()):
                    serializer.is_occupied = True
                else:
                    serializer.is_occupied = False
                serializer['is_occupied'] = serializer.is_occupied
            result.append(serializer)
        return Response(status=HTTPStatus.OK, data=result)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reserv_room_start = ReservationRoom.objects.filter(
            day=request.data['day'],
            start_reservation=request.data['start_reservation']
        ).first()
        reserv_room_end = ReservationRoom.objects.filter(
            day=request.data['day'],
            end_reservation=request.data['end_reservation']
        ).first()
        if reserv_room_end or reserv_room_start:
            return Response(status=HTTPStatus.BAD_REQUEST, data='Переговорная уже зарезервирована')
        self.perform_create(serializer)
        user_id = User.objects.filter(id=request.data['user']).first()
        meetingroom_id = MeetingRoom.objects.filter(id=request.data['meetingroom']).first()
        period_reservation = f'день {request.data["day"]} -{request.data["start_reservation"]} - {request.data["end_reservation"]}'
        LogForMeetingRoom.objects.create(
            user=user_id,
            meetingroom=meetingroom_id,
            period_reservation=period_reservation,
            informations=f'Пользователь {user_id.username} забронировал переговорную {meetingroom_id}, дата брони {period_reservation}'
        )
        return Response(serializer.data, status=HTTPStatus.CREATED)


class LogViewSet(viewsets.ModelViewSet):
    queryset = LogForMeetingRoom.objects.all()
    serializer_class = LogSerializer

    @swagger_auto_schema(request_body=no_body)
    @action(detail=False, methods=('get',), url_path='get_report',  url_name='get_report')
    def get_report(self, request):
        create_report()
        return Response(data='Отчет готов', status=HTTPStatus.OK)