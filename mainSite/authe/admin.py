from django.contrib import admin
from .models import CustomerUser, CustomerDog, PossibleAllergies, CustomerCart



admin.site.register(CustomerUser)
admin.site.register(CustomerCart)
admin.site.register(CustomerDog)
admin.site.register(PossibleAllergies)