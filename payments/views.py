from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Payment
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class PaymentsListView(ListView):
    model = Payment
    template_name = 'payments/home.html'
    context_object_name = 'payments'
    ordering = ['-trans_date']
    paginate_by = 5
