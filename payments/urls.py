from django.urls import path
from . import views
from .views import (
    PaymentsListView
)

urlpatterns = [
    path('', PaymentsListView.as_view(), name="payments-home"),
]
