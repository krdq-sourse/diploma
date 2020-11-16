from django.urls import path

from . import views


urlpatterns = [
    path("app/", views.ApplicationListView.as_view()),
    path("addapp/", views.AddApplicationView.as_view())

]