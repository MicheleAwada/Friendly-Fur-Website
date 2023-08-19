from django.shortcuts import render

# Create your views here.
def shopPage(request):
    return render(request, 'shop/shop.html')