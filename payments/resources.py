from import_export import resources
from .models import Payment, Ticket
from companies.models import CompanyUser, Region
from django.db.models import F
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = ['trans_id', 'payer_account', 'payer_name', 'payee_account', 'payee_name', 'amount',
                  'record_date', 'trans_date', 'author', 'company', 'ticket_issued', 'channel', 'receipt_no']


class TicketResource(resources.ModelResource):
    trans_id = fields.Field(column_name='Trans ID', attribute='payment',
                            widget=ForeignKeyWidget(Payment, 'trans_id'))
    issuer = fields.Field(column_name='Issuer', attribute='issuer',
                          widget=ForeignKeyWidget(CompanyUser, 'user__username'))
    region = fields.Field(column_name='Region', attribute='region',
                          widget=ForeignKeyWidget(Region, 'name'))
    issue_date = fields.Field(column_name='Issue Date', attribute='issue_date')
    unit_price = fields.Field(column_name='Unit Price', attribute='unit_price')
    ticket_value = fields.Field(column_name='Amount', attribute='ticket_value')
    ticket_count = fields.Field(
        column_name='Ticket Count', attribute='ticket_count')
    balance = fields.Field(column_name='Balance', attribute='balance')

    class Meta:
        model = Ticket
        fields = ['trans_id', 'region', 'issue_date', 'ticket_value',
                  'unit_price', 'ticket_count', 'balance', 'issuer']
        widgets = {
            'Issue Date': {'format': '%d.%m.%Y'},
        }

    def get_queryset(self):
        return Ticket.objects.all()
