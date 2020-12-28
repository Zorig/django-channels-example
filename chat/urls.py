from django.urls import path

from .views import ChatList, ChatRoom, CreateRoom

app_name = "chat"

urlpatterns = [
    path("", ChatList.as_view(), name="index"),
    path("create/", CreateRoom.as_view(), name="create"),
    path("<slug>/", ChatRoom.as_view(), name="room"),
]
