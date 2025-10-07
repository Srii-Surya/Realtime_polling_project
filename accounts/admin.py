from django.contrib import admin
from .models import Organizer
from django.contrib.auth.admin import UserAdmin
admin.site.register(Organizer, UserAdmin)
