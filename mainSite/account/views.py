from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from django.core.mail import send_mail
from .forms import changeName
from django.contrib import messages
# Create your views here.

@login_required
def account_detail(request):
    if request.method == "POST":
        form = changeName(request.POST, instance=request.user)
        if form.is_valid():
            fullname = form.cleaned_data.get("full_name")
            form.save()
            messages.success(request, "Full Name Successfully changed to "+ str(fullname))
            return redirect(reverse("account-detail"))
    else:
        form = changeName(initial={"full_name":request.user.getfullname()})
    context={"form":form,}
    return render(request, 'account/account-detail.html', context)