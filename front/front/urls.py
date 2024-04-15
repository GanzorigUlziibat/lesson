
from django.urls import path
from lesson.views import *
urlpatterns = [
    path('', dt_login),
    path('dashboard/', dt_dashboard, name="dashboard"),
    path('register/', dt_register, name="register")
]
