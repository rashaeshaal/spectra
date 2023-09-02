from django.contrib import admin
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
# Register your models here.
admin.site.register (get_user_model())