from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Company, Region, CompanyUser
from users.models import Role


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'company', 'price']
        widgets = {
            'company': forms.HiddenInput,
        }


def company_roles():
    list = Role.objects.filter(is_internal=False).all()
    roles = map(lambda r: (r.id, r.name), list)
    return roles


class AddCompanyUserForm(forms.Form):
    def __init__(self, company_id=None, *args, **kwargs):
        super(AddCompanyUserForm, self).__init__(*args, **kwargs)
        regions = Company.objects.filter(pk=company_id).first().region_set.all()
        self.fields['region'] = forms.ChoiceField(choices=map(lambda r: (r.id, r.name), regions))
        self.fields['username'] = forms.CharField()
        self.fields['email'] = forms.EmailField()
        self.fields['role'] = forms.ChoiceField(choices=company_roles())
