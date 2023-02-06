from django.contrib import admin
from main.models import CustomUser, Gender, DayOfWeek, WorkingHours, Rest, MasterShadow

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Gender)
admin.site.register(DayOfWeek)
admin.site.register(WorkingHours)
admin.site.register(Rest)
admin.site.register(MasterShadow)