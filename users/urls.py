"""defines patterns of addresses URL for app users."""
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    #Adding default adresses URL of authentication
    path('', include('django.contrib.auth.urls')),
    #Registration page
    path('register/', views.register, name='register'),
]