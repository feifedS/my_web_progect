from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Gender)
admin.site.register(DayOfWeek)
admin.site.register(WorkingHours)
admin.site.register(Rest)
admin.site.register(MasterShadow)
admin.site.register(TypesOfServices)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Status)
admin.site.register(Barber)
admin.site.register(Booking)
# admin.site.register(AvailableTimeSlot)