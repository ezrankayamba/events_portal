from import_export import resources
from .models import Payment, Ticket
from companies.models import CompanyUser, Region
from django.db.models import F
from import_export import fields, resources
from import_export import widgets
# from import_export.widgets import ForeignKeyWidget


class PaymentResource(resources.ModelResource):
    trans_id = fields.Field(column_name='Trans ID', attribute='trans_id')
    channel = fields.Field(column_name='Channel', attribute='channel')
    receipt_no = fields.Field(column_name='Rceipt No', attribute='receipt_no')
    payer_account = fields.Field(
        column_name='Payer MSISDN', attribute='payer_account')
    payer_name = fields.Field(column_name='Payer Name', attribute='payer_name')
    trans_date = fields.Field(column_name='Trans Date', attribute='trans_date',
                              widget=widgets.DateTimeWidget(format='%d/%m/%Y %H:%M'))
    amount = fields.Field(column_name='Amount', attribute='amount')
    ticket_issued = fields.Field(
        column_name='Ticket Issued', attribute='ticket_issued')

    def __init__(self, user):
        self.user = user

    class Meta:
        model = Payment
        fields = ['trans_id', 'channel', 'receipt_no', 'payer_account', 'payer_name', 'trans_date',
                  'amount', 'ticket_issued']

    def get_queryset(self):
        if self.user:
            role = self.user.profile.role
            if role:
                if role.is_internal:
                    return Payment.objects.all().order_by('-trans_date')
                else:
                    company = self.user.companyuser.company
                    return Payment.objects.filter(company=company).order_by('-trans_date')
        print('Not allowed to export!')
        return []


class TicketResource(resources.ModelResource):
    trans_id = fields.Field(column_name='Trans ID', attribute='payment',
                            widget=widgets.ForeignKeyWidget(Payment, 'trans_id'))
    issuer = fields.Field(column_name='Issuer', attribute='issuer',
                          widget=widgets.ForeignKeyWidget(CompanyUser, 'user__username'))
    region = fields.Field(column_name='Region', attribute='region',
                          widget=widgets.ForeignKeyWidget(Region, 'name'))
    issue_date = fields.Field(column_name='Issue Date', attribute='issue_date',
                              widget=widgets.DateTimeWidget(format='%d/%m/%Y %H:%M'))
    unit_price = fields.Field(column_name='Unit Price', attribute='unit_price')
    ticket_value = fields.Field(column_name='Amount', attribute='ticket_value')
    ticket_count = fields.Field(
        column_name='Ticket Count', attribute='ticket_count')
    balance = fields.Field(column_name='Balance', attribute='balance')

    def __init__(self, user):
        self.user = user

    class Meta:
        model = Ticket
        fields = ['trans_id', 'region', 'issue_date', 'ticket_value',
                  'unit_price', 'ticket_count', 'balance', 'issuer']

    def get_queryset(self):
        if self.user:
            role = self.user.profile.role
            print(f'User: {self.user}, Role: {role}')
            if role:
                if role.is_internal:
                    return Ticket.objects.all().order_by('-issue_date')
                else:
                    region = self.user.companyuser.region
                    return Ticket.objects.filter(region=region).order_by('-issue_date')
        print('Not allowed to export!')
        return []
