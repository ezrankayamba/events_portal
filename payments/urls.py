from django.urls import path
from . import views
from .views import (
    PaymentsListView,
    MyCompanyPaymentListView,
    MyCompanyTicketsListView
)

urlpatterns = [
    path('', PaymentsListView.as_view(), name="payments-home"),
    path('company/<int:company_id>/payments',
         MyCompanyPaymentListView.as_view(), name="company-payments"),
    path('company/<int:company_id>/tickets',
         MyCompanyTicketsListView.as_view(), name="company-tickets"),
]
