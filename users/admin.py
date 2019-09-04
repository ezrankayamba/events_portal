from django.contrib import admin
from .models import Profile, Permission, Role

admin.site.register(Profile)
admin.site.register(Permission)
admin.site.register(Role)
