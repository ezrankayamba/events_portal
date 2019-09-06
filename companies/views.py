from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Company, Region, CompanyUser
from django.contrib.auth.models import User
from django import forms
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class CompanyListView(ListView):
    model = Company
    template_name = 'companies/home.html'
    context_object_name = 'companies'
    ordering = ['-name']
    paginate_by = 5


class CompanyDetailView(DetailView):
    model = Company


class CompanyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    success_url = '/companies'

    def test_func(self):
        return True


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    fields = ['name', 'account', 'email', 'password']

    def form_valid(self, form):
        return super().form_valid(form)


class CompanyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Company
    fields = ['name', 'account', 'email', 'password']

    def form_valid(self, form):
        return super().form_valid(form)

    def test_func(self):
        return True

# Regions


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['name', 'company', 'price', 'company_users']
        widgets = {
            'company': forms.HiddenInput,
        }


class RegionCreateView(LoginRequiredMixin, CreateView):
    model = Region
    form_class = RegionForm

    def get_initial(self, *args, **kwargs):
        initial = super(RegionCreateView, self).get_initial(**kwargs)
        initial['company'] = self.kwargs.get('company_id')
        return initial

    def form_valid(self, form):
        return super().form_valid(form)
