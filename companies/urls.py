from django.urls import path
from . import views
from .views import (
    CompanyListView,
    CompanyDetailView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView
)

urlpatterns = [
    path('', CompanyListView.as_view(), name="companies-home"),
    path('<int:pk>/', CompanyDetailView.as_view(), name="company-detail"),
    path('new/', CompanyCreateView.as_view(), name="company-create"),
    path('<int:pk>/update', CompanyUpdateView.as_view(), name="company-update"),
    path('<int:pk>/delete', CompanyDeleteView.as_view(), name="company-delete"),
]
