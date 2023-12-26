from django.contrib import admin
from django.contrib.sessions.models import Session
from accounts.models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Session)