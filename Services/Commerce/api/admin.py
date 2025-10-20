from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.

admin.site.register(Commerce)
admin.site.register(CommerceFiles)
admin.site.register(CommerceComments)
admin.site.register(CommerceVotes)

