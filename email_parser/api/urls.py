from django.urls import path
from .views import EmailDataAPI

urlpatterns = [
    path('', EmailDataAPI.as_view())
]
