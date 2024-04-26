from django.contrib import admin
from .models import videoSettings, User_Credentials

# Register your models here.
admin.site.register(videoSettings)
admin.site.register(User_Credentials)