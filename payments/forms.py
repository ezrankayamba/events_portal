from django import forms
from django.contrib.auth.models import User
from .models import Ticket, Payment
from django.core.validators import RegexValidator

# ^255(6|7)\d{8}$


class IssueTicketForm(forms.Form):
    payer_account = forms.CharField(
        label="Enter customer phone number e.g. 255711000222",
        validators=[RegexValidator(r'^255(6|7)\d{8}$', message="Enter valid MSISDN e.g. 255711000222")]
    )
    trans_id = forms.CharField(
        label="Transaction ID from service provider of the sernder",
        validators=[RegexValidator(r'^((?!ON-NET).)*$', message="Enter valid Transaction ID")]
    )
