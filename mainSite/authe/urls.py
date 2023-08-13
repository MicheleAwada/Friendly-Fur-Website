from django.contrib.auth import urls as autheUrls
from django.urls import path, include

urlpatterns = [
    path("", include(autheUrls))

]
