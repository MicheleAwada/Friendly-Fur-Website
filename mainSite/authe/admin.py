from django.contrib import admin
from .models import CustomerUser, CustomerDog, PossibleAllergies, PossibleBreeds, CustomerCart, UnverifiedUser



admin.site.register(UnverifiedUser)
admin.site.register(CustomerUser)
admin.site.register(CustomerCart)
admin.site.register(CustomerDog)
admin.site.register(PossibleAllergies)
admin.site.register(PossibleBreeds)