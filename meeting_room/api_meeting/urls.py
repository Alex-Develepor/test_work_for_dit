from rest_framework.routers import DefaultRouter

from .views import LogViewSet, MeetingRoomView, ReservationMeetingRoomView

router = DefaultRouter()

router.register(
    r'MeetingRoom',
    MeetingRoomView,
    basename='meetingroom'
)

router.register(
    r'ReservationMeetingRoom',
    ReservationMeetingRoomView,
    basename='reservationmeetingroom'
)

router.register(
    r'LogViewSet',
    LogViewSet,
    basename='LogViewSet'
)
urlpatterns = router.urls
