from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Company, Region, CompanyUser
from users.models import Role


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'company', 'price', 'region_users']
        widgets = {
            'company': forms.HiddenInput,
        }


def company_roles():
    list = Role.objects.filter(is_internal=False).all()
    roles = map(lambda r: (r.id, r.name), list)
    return roles


class AddCompanyUserForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    role = forms.ChoiceField(choices=company_roles())
