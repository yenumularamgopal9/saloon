# salon/admin.py
from django.contrib import admin
from .models import AdminUser, UserProfile, Service, AvailableSlot, Booking, Checkout, UserHistory

admin.site.register(AdminUser)
admin.site.register(UserProfile)
admin.site.register(Service)
admin.site.register(AvailableSlot)
admin.site.register(Booking)
admin.site.register(Checkout)
admin.site.register(UserHistory)
