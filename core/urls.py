from django.contrib import admin
from django.urls import path
from core.views import command_view
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    
    path('', command_view, name='command_view'),
    
]

