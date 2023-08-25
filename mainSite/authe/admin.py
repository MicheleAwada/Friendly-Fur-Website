from django.contrib import admin
from .models import CustomerUser, CustomerDog, PossibleAllergies



admin.site.register(CustomerUser)
admin.site.register(CustomerDog)
admin.site.register(PossibleAllergies)