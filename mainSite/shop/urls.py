from django.urls import path
from .views import shopPage
urlpatterns = [
    path("", shopPage, name="shop"),
]