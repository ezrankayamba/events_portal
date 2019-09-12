from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Payment, Ticket
from companies.models import Company
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import IssueTicketForm
from django.urls import reverse
from django.contrib import messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.http import HttpResponse
from .resources import PaymentResource, TicketResource
from django.db.models import Q


class PaymentsListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/home.html'
    context_object_name = 'payments'
    ordering = ['-trans_date']
    paginate_by = 5


class CompanyPaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/home.html'
    context_object_name = 'payments'
    ordering = ['-trans_date']
    paginate_by = 5

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('company_id'))
        return Payment.objects.filter(company=company).order_by('-trans_date')


class UserTicketingFormListView(LoginRequiredMixin, FormView):
    form_class = IssueTicketForm
    template_name = 'payments/ticketing.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super(UserTicketingFormListView, self).get_initial(**kwargs)
        company_id = self.kwargs.get('company_id')
        self.company = Company.objects.filter(pk=company_id).first()
        self.success_url = reverse('user-ticketing', kwargs={'company_id': company_id})
        return initial

    def get_context_data(self, **kwargs):
        company_id = self.kwargs.get('company_id')
        kwargs['company'] = Company.objects.filter(pk=company_id).first()
        kwargs['tickets'] = Ticket.objects.filter(issuer=self.request.user.companyuser).order_by('-issue_date')
        return super(UserTicketingFormListView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        user = self.request.user
        data = form.cleaned_data
        print('Cleaned data: ', data)
        if data['trans_id'].strip() == 'ON-NET':
            messages.warning(self.request, f'Failed, "ON-NET" is not valid Transaction ID')
        else:
            payment = Payment.objects.filter(Q(payer_account=data['payer_account']), Q(trans_id=data['trans_id']) | Q(receipt_no=data['trans_id'])).first()
            if payment:
                print('Payment: ', payment.amount)
                cu = user.companyuser
                unit_price = cu.region.price
                count = int(payment.amount / unit_price)
                balance = payment.amount - (count * unit_price)
                if payment.ticket_issued:
                    messages.warning(self.request, 'Alert, The ticket(s) for this payment already issued!')
                elif not count:
                    messages.warning(self.request, 'Fail, not enough amount to purchase a ticket!')
                else:
                    ticket = Ticket(payment=payment, unit_price=unit_price, ticket_value=payment.amount, ticket_count=count, balance=balance, issuer=cu, region=cu.region)
                    ticket.save()
                    payment.ticket_issued = True
                    payment.save()
                    messages.success(self.request, f'Success, you have successfully issued {count} ticket(s)!')
            else:
                messages.warning(self.request, 'Failed, review your inputs and resubmit!')
        return super().form_valid(form)


class CompanyTicketsListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'payments/tickets.html'
    context_object_name = 'tickets'
    ordering = ['-issue_date']
    paginate_by = 5

    def get_queryset(self):
        company = get_object_or_404(Company, id=self.kwargs.get('company_id'))
        return Ticket.objects.filter(payment__company=company).order_by('-issue_date')


class AllTicketsListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'payments/tickets.html'
    context_object_name = 'tickets'
    ordering = ['-issue_date']
    paginate_by = 5

    def get_queryset(self):
        return Ticket.objects.order_by('-issue_date')


def export_payments(request):
    resource = PaymentResource()
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'
    return response


def export_tickets(request):
    resource = TicketResource()
    # result = Ticket.objects.select_related('payment')
    dataset = resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tickets.csv"'
    return response
