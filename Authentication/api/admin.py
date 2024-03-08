from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
 
admin.site.register(LegalUser)
admin.site.register(Wallet)
admin.site.register(User)
admin.site.register(OTPRequest)