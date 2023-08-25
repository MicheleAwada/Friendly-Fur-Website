from django.urls import path
from .views import shopPage, product_detail
urlpatterns = [
    path("", shopPage.as_view(), name="shop"),
    path("product/<slug:slug>/", product_detail, name='product-detail')
]