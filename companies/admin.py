from django.contrib import admin
from .models import Company, CompanyUser, Region


admin.site.register(Company)
admin.site.register(CompanyUser)
admin.site.register(Region)
