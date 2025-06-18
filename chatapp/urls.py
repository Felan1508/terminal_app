
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
import os



urlpatterns = [
    path('', views.room_selector, name='room_selector'),  # ✅ for /chat/
    path('<str:room_name>/', views.room, name='room'),     # ✅ for /chat/room1/
]

