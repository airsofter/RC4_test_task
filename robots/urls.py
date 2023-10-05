from django.urls import path

from .views import NewRobot


urlpatterns = [
    path('', NewRobot.as_view())
]
