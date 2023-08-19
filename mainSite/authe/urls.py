from django.contrib.auth import urls as autheUrls
from django.urls import path, include
from .views import signup, account, CustomLoginView, CustomLogoutView
urlpatterns = [
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name='logout'),
    path("", include(autheUrls)),
    path("signup/", signup, name='signup'),
    path("temp/", account),
]
