from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product, Brand
from authe.models import CustomerCart
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

class cartPage(TemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.request.user.cart.all()
        return context
class shopPage(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productcount = Product.objects.all().count()
        context['products'] = Product.objects.all()[:50]
        return context

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # images_url = [image for product.images.all().image.url]
    return render(request, 'shop/product_detail.html', {'product': product,})

def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    products = brand.brand_prodcuts.all();
    # images_url = [image for product.images.all().image.url]
    return render(request, 'shop/brand_detail.html', {'brand': brand,'products':products})


def search_view(request):
    products = Product.objects
    raw_query = request.GET.get('q')
    did_something=[]
    if raw_query:
        query = SearchQuery(raw_query, search_type='phrase')
        if query:
            did_something.append(True)
            products = products.annotate(
                search=SearchVector("title") + SearchVector("description") + SearchVector("product_ingredients__name") + SearchVector("brand__name")
            ).filter(search=query)
    raw_filter = request.GET.get('f','')
    filters = raw_filter.split(",")
    if raw_filter:
        defaults = [0,-1]
        for i in range(2):
            filters[i]=int(filters[i])
        for i, (default, value) in enumerate(zip(defaults, filters)):
            if default!=value:
                did_something.append(True)
                if i==0: #price min
                    products = products.filter(price__gt=value)
                if i==1: #price max
                    products = products.filter(price__lt=value)

    if not any(did_something):
        products= products.all()
    context = {'products': products,'query': raw_query}
    return render(request, 'shop/search_results.html', context)

@login_required
def addtocart(request, slug):
    product = Product.objects.filter(slug=slug).first()
    if product:
        if request.user.user_cart.filter(product__slug=slug):
            print("truh")
            existing_product = request.user.user_cart.filter(product__pk=product.pk).first()
            if not (existing_product.quantity > product.quantity):
                existing_product.quantity+=1
                existing_product.save()
                print("hachu")
            else:
                return render(request, 'shop/cart_product_error.html')
        else:
            new_cart = CustomerCart(quantity=1, product=product)
            new_cart.save()
            request.user.user_cart.add(new_cart)
    else:
        return render(request, 'shop/cart_product_error.html')


    context = {'product':product}
    return render(request, 'shop/cart_add.html', {'product': product})
