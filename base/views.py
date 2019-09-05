from django.shortcuts import render
from companies.models import Company


def home(request):
    context = {
        'companies': Company.objects.all()
    }
    return render(request, 'base/home.html', context)
