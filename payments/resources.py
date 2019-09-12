from import_export import resources
from .models import Payment, Ticket
from django.db.models import F


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment


class TicketResource(resources.ModelResource):
    class Meta:
        model = Ticket
        fields = ['payment__trans_id', 'region__name', 'issue_date', 'ticket_value', 'unit_price', 'ticket_count', 'balance', 'issuer__user__username']
