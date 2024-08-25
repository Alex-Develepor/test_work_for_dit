from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import LogForMeetingRoom, MeetingRoom, ReservationRoom, User


class MeetingRoomSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20),

    class Meta:
        model = MeetingRoom
        fields = '__all__'


class GetBookingSerializers(serializers.ModelSerializer):
    day = serializers.DateField(required=True)
    is_occupied = serializers.BooleanField(default=False)
    time = serializers.TimeField(required=True)
    start_reservation = serializers.TimeField()
    end_reservation = serializers.TimeField()
    user = UserSerializer()
    meetingroom = MeetingRoomSerializer(required=True)

    def validate(self, data):
        if data['is_occupied']:
            raise serializers.ValidationError('Комната уже занята.')
        return data

    def create(self, validated_data):
        room = ReservationRoom(**validated_data)
        room.save()
        return room

    def update(self, instance, validated_data):
        instance.is_occupied = validated_data.get('is_occupied', False)
        instance.save()
        return instance

    class Meta:
        model = ReservationRoom
        fields = '__all__'
        required_fields = ['day', 'time']


class GetReservationRoomSerializer(serializers.ModelSerializer):
    day = serializers.DateField()
    start_reservation = serializers.TimeField()
    end_reservation = serializers.TimeField()
    user = UserSerializer()
    meetingroom = MeetingRoomSerializer()

    class Meta:
        model = ReservationRoom
        fields = '__all__'


class CreateReservationRoomSerializer(serializers.ModelSerializer):
    day = serializers.DateField()
    start_reservation = serializers.TimeField()
    end_reservation = serializers.TimeField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    meetingroom = serializers.PrimaryKeyRelatedField(queryset=MeetingRoom.objects.all())

    class Meta:
        model = ReservationRoom
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogForMeetingRoom
        fields = '__all__'
