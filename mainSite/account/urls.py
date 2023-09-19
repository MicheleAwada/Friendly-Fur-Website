from django.urls import path
from . import views
urlpatterns = [
    path('details/', views.account_detail, name="account-detail"),
]