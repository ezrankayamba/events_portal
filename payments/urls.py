from django.urls import path
from . import views
from .views import (
    PaymentsListView,
    CompanyPaymentListView,
    CompanyTicketsListView,
    UserTicketingFormListView,
    AllTicketsListView
)

urlpatterns = [
    path('', PaymentsListView.as_view(), name="payments-home"),
    path('company/<int:company_id>/payments', CompanyPaymentListView.as_view(), name="company-payments"),
    path('company/<int:company_id>/tickets', CompanyTicketsListView.as_view(), name="company-tickets"),
    path('tickets', AllTicketsListView.as_view(), name="all-tickets"),
    path('company/<int:company_id>/ticketing', UserTicketingFormListView.as_view(), name="user-ticketing"),
    path('exportpayments/', views.export_payments, name='export-payments'),
    path('exporttickets/', views.export_tickets, name='export-tickets'),
]
