from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def homePage(request):
    return render(request, "home/home.html")