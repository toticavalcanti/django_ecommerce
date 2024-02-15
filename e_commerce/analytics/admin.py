from django.contrib import admin
from .models import UserSession
from .models import ObjectViewed
admin.site.register(ObjectViewed)
admin.site.register(UserSession)
