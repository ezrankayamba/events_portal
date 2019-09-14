from import_export import resources
from .models import Payment, Ticket
from companies.models import CompanyUser, Region
from django.db.models import F
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget


class PaymentResource(resources.ModelResource):
    trans_id = fields.Field(column_name='Trans ID', attribute='trans_id')
    channel = fields.Field(column_name='Channel', attribute='channel')
    receipt_no = fields.Field(column_name='Rceipt No', attribute='receipt_no')
    payer_account = fields.Field(
        column_name='Payer MSISDN', attribute='payer_account')
    payer_name = fields.Field(column_name='Payer Name', attribute='payer_name')
    trans_date = fields.Field(column_name='Trans Date', attribute='trans_date')
    amount = fields.Field(column_name='Amount', attribute='amount')
    ticket_issued = fields.Field(
        column_name='Ticket Issued', attribute='ticket_issued')

    class Meta:
        model = Payment
        fields = ['trans_id', 'channel', 'receipt_no', 'payer_account', 'payer_name', 'trans_date',
                  'amount', 'ticket_issued']


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
