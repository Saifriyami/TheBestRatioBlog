from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view_file/<str:filename>/', views.view_file, name='view_file'),
]