from django.contrib import admin
from .models import Doctor, Specialities, Address, Booking, Slot

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialities)
admin.site.register(Address)
admin.site.register(Booking)
admin.site.register(Slot)