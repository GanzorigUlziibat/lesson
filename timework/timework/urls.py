
from django.contrib import admin
from django.urls import path
from timeapp.views import index

urlpatterns = [
    path('timeapp/', index),
]
