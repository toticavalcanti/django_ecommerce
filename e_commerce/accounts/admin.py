from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import GuestEmail
User = get_user_model()
admin.site.register(User)
admin.site.register(GuestEmail)
# Register your models here.
