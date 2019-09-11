from django.urls import path
from . import views
from .views import (
    CompanyListView,
    CompanyDetailView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    RegionCreateView,
    CompanyUserCreateView,
    CompanyUserUpdateView,
    RegionUpdateView
)

urlpatterns = [
    path('', CompanyListView.as_view(), name="companies-home"),
    path('<int:pk>/', CompanyDetailView.as_view(), name="company-detail"),
    path('new/', CompanyCreateView.as_view(), name="company-create"),
    path('<int:pk>/update', CompanyUpdateView.as_view(), name="company-update"),
    path('<int:pk>/delete', CompanyDeleteView.as_view(), name="company-delete"),
    path('<int:company_id>/regions/new', RegionCreateView.as_view(), name="region-create"),
    path('<int:company_id>/user/new', CompanyUserCreateView.as_view(), name="company-user-create"),
    path('user/<int:pk>/update', CompanyUserUpdateView.as_view(), name="company-user-update"),
    path('region/<int:pk>/update', RegionUpdateView.as_view(), name="region-update"),
]
