from django.contrib import admin
from .models import Product, AboutProduct, ProductImages, Brand
admin.site.register(Product)
admin.site.register(AboutProduct)
admin.site.register(ProductImages)
admin.site.register(Brand)