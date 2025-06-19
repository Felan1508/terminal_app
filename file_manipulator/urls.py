from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_files, name='list_files'),
    path('edit/<str:filename>/', views.edit_file, name='edit_file'),
]
