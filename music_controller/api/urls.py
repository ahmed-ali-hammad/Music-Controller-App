from django.urls import path, include
from .views import *

app_name = "api"

urlpatterns = [
    path('room/list/', RoomAPIView.as_view()),
    path('room/create/', RoomCreateAPIView.as_view()),
    path('room/update/', RoomUpdateAPIView.as_view()),
    path('room/detail/<str:code>/', RoomRetrieveApiView.as_view()),
    path('room/join/', RoomJoinAPIView.as_view()),
    path('room/user/in/', UserInRoomAPIView.as_view()),
    path('room/leave/', LeaveRoomAPIView.as_view()),

]
