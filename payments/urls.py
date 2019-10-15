from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentsListView.as_view(), name="payments-home"),
    path('company/<int:company_id>/payments', views.CompanyPaymentListView.as_view(), name="company-payments"),
    path('company/<int:company_id>/tickets', views.CompanyTicketsListView.as_view(), name="company-tickets"),
    path('tickets', views.AllTicketsListView.as_view(), name="all-tickets"),
    path('company/<int:company_id>/ticketing', views.UserTicketingFormListView.as_view(), name="user-ticketing"),
    path('exportpayments/', views.export_payments, name='export-payments'),
    path('exporttickets/', views.export_tickets, name='export-tickets'),
    path('manualentry/', views.ManualEntryFormView.as_view(), name='manualentry-payment'),
]
