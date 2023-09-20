from django.contrib.auth import urls as autheUrls
from django.urls import path, include
from .views import signup, CustomLoginView, CustomLogoutView, email_verification, is_email_valid, autocomplete_ajax
from . import views
urlpatterns = [
    path("delete_account/", views.delete_user, name="delete_user"),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name='logout'),
    path("", include(autheUrls)),
    path("signup/", signup, name='signup'),
    path("email_change/", views.email_change, name='email_change'),
    path("verify/<uid64>/<token>/", email_verification, name='verify'),
    path("is_email_valid/", is_email_valid, name='is_email_valid'),
    path("autocomplete_ajax /", autocomplete_ajax, name="autocomplete-ajax"),
    path("dog/signup/", views.signdogup, name="signdogup"),
    path("dog/delete/<dog_number>/", views.deletedog, name="dogdelete"),
]
