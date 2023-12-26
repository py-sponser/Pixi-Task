from django.contrib import admin
from training.models import *
# Register your models here.

admin.site.register(TrainingProvider)
admin.site.register(Course)
admin.site.register(UserCourse)