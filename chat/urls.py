from django.urls import path
from chat.views import *

urlpatterns = [
    path('room/', Rooms.as_view()),
    path('dialog/', Dialog.as_view()),
    path('users/', AddUsersRoom.as_view()),
]