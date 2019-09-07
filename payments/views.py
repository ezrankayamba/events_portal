from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Payment, Ticket
from companies.models import Company
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class PaymentsListView(ListView):
    model = Payment
    template_name = 'payments/home.html'
    context_object_name = 'payments'
    ordering = ['-trans_date']
    paginate_by = 5


class MyCompanyPaymentListView(ListView):
    model = Payment
    template_name = 'payments/home.html'
    context_object_name = 'payments'
    ordering = ['-trans_date']
    paginate_by = 5

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('company_id'))
        return Payment.objects.filter(company=company).order_by('-trans_date')


class MyCompanyTicketsListView(ListView):
    model = Ticket
    template_name = 'payments/tickets.html'
    context_object_name = 'tickets'
    ordering = ['-issue_date']
    paginate_by = 5

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('company_id'))
        return Ticket.objects.filter(payment__company=company).order_by('-issue_date')
