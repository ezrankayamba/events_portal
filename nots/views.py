from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TransType
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class TransTypeListView(ListView):
    model = TransType
    template_name = 'companies/home.html'
    context_object_name = 'companies'
    ordering = ['-regex_key']
    paginate_by = 5


class TransTypeDetailView(DetailView):
    model = TransType


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


class RegionCreateView(LoginRequiredMixin, CreateView):
    model = Region
    form_class = RegionForm

    def get_initial(self, *args, **kwargs):
        initial = super(RegionCreateView, self).get_initial(**kwargs)
        initial['company'] = self.kwargs.get('company_id')
        return initial

    def get_context_data(self, **kwargs):
        company_id = self.kwargs.get('company_id')
        kwargs['company'] = Company.objects.filter(pk=company_id).first()
        return super(RegionCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class CompanyUserCreateView(LoginRequiredMixin, FormView):
    form_class = AddCompanyUserForm
    template_name = 'companies/user_form.html'
    success_url = '/'

    def get_initial(self, *args, **kwargs):
        initial = super(CompanyUserCreateView, self).get_initial(**kwargs)
        company_id = self.kwargs.get('company_id')
        self.company = Company.objects.filter(pk=company_id).first()
        self.success_url = reverse('company-detail', kwargs={'pk': company_id})
        return initial

    def get_context_data(self, **kwargs):
        company_id = self.kwargs.get('company_id')
        kwargs['company'] = Company.objects.filter(pk=company_id).first()
        return super(CompanyUserCreateView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        print('Cleaned data: ', form.cleaned_data)
        user = User(username=data['username'], email=data['email'])
        user.set_password('testing321')
        user.save()
        profile = user.profile
        profile.role = Role.objects.get(pk=data['role'])
        profile.save()
        company_user = CompanyUser(user=user, company=self.company)
        company_user.save()
        return super().form_valid(form)
