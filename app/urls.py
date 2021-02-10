from django.urls import path
from django.urls import re_path, include
from . import views
from .views import RegistrationAPIView
from .views import LoginAPIView


urlpatterns = [
    path("app/", views.ApplicationListView.as_view()),
    path("addapp/", views.AddApplicationView.as_view()),
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),

]