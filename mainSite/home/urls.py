from django.contrib.auth import urls as autheUrls
from django.urls import path
from .views import homePage
urlpatterns = [
    path("home/", homePage, name="home")
]