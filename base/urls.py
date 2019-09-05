from django.urls import path, include
from . import views
from .views import home

urlpatterns = [
    path('', home, name="base-home"),
]
