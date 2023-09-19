from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.shopPage.as_view(), name="shop"),
    path("product/<slug:slug>/", views.product_detail, name='product'),
    path("brand/<slug:slug>/", views.brand_detail, name='brand'),
    path('search/', views.search_view, name='search'),
    path('cart/', views.cartPage.as_view(), name='cart'),
    path('cart/added/<slug:slug>', views.addtocart, name='added_to_cart'),
]