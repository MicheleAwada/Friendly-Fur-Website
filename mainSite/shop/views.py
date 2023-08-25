from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Product
from django.shortcuts import get_object_or_404
# Create your views here.
class shopPage(TemplateView):
    template_name = 'shop/shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})