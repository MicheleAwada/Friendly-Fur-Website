import base64
from django.shortcuts import render,redirect, reverse
from .forms import UserRegisterForm,CustomerDogForm, EmailChange
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group
from .models import CustomerUser, PossibleAllergies, UnverifiedUser, PossibleBreeds
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.core.validators import EmailValidator
from .models import limit_ajax_email_validators
from django.contrib.auth.tokens import default_token_generator
import secrets
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404

@login_required
def delete_user(request):
    if request.method=="POST":
        request.user.delete()
        messages.success(request, "Account delete")
        return redirect("/")
    return render(request, "authe/delete_user.html", {"name": request.user.first_name})

@login_required
def signdogup(request):
    if request.method=="POST":
        form = CustomerDogForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, f"Success! Recommendations will now be catered to {form.cleaned_data.get('name')}")
            return redirect("/")
    else:
        form = CustomerDogForm()
    return render(request, "authe/signdogup.html", {"form":form})
@login_required
def deletedog(request, dog_number):
    dog = request.user.dogs.filter(dog_number=dog_number)
    if dog.count()!=1:
        raise Http404
    dog = dog.first()
    if request.method=="POST":
        dog.delete()
        messages.success(request, f"Success, {dog.name} was deleted")
        return redirect(reverse('account-detail'))
    else:
        return render(request, "authe/dogdelete.html", {"dog":dog})
def autocomplete_ajax(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            allergy = data.get('allergy',None)
            breed = data.get('breed',None)
            if allergy:
                model = PossibleAllergies
                query = allergy
            elif breed:
                model = PossibleBreeds
                query = breed
            else:
                return HttpResponseBadRequest('Invalid request')
            search = model.objects.filter(Q(name__icontains=query))
            if search.exists():
                returns = [[entry.name,entry.color] for entry in search]
                returns1 = [a[0] for a in returns]
                returns2 = [a[1] for a in returns]
                returns = [returns1, returns2]
            else:
                returns = [[],[]]
            return JsonResponse({"results":returns})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
def is_email_valid(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'POST':
            ip_address = request.META.get('REMOTE_ADDR')
            ip, created = limit_ajax_email_validators.objects.get_or_create(ip=ip_address)
            if not created:
                if ip.is_banned(): return


            data = json.load(request)
            email = data.get('email')
            email_validator = EmailValidator()
            if not email:
                return JsonResponse({'is_email_valid': 3})
            if CustomerUser.objects.filter(email=email).exists():
                return JsonResponse({'is_email_valid': 1})
            return JsonResponse({'is_email_valid': 0})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')



def signup(request):
    redirect_after = reverse('signup')
    if request.user.is_authenticated:
        return render(request, "authe/alreadylogged.html", {'redirect': redirect_after})
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            full_name = form.cleaned_data.get("full_name")
            print(user.email)
            url = user.get_url()
            email = EmailMessage("Account Created For Friendly Fur",
                         f"Hello {full_name}, We're Glad your deciding to spoil your dog by using Friendly Fur;)\n"+
                         f"Verification Link: {url}",
                         "noreply@friendlyfur.com",
                         [user.email])
            email.send()
            messages.success(request, f"Account created. Verify via email. CHEATCHEAT -> verify now: {url}")
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "authe/signup.html", {'form': form})
@login_required
def email_change(request):
    if request.method=="POST":
        form = EmailChange(request.POST, user=request.user)
        if form.is_valid():
            old_email = request.user.email
            new_email = form.cleaned_data.get("email")
            unverf_user = form.save(request.user)
            sent_email_confirmation = EmailMessage("Email Change", f"A email change for Friendly Fur\n{unverf_user.get_url()}\nIf this wasn't you, you may safely ignore this email\n", "noreply@FriendlyFur.com", to=[new_email])
            sent_email_confirmation.send()
            sent_email = EmailMessage("Email Change", f"A email change for Friendly Fur was requested\nfrom (this email) {old_email} to {new_email}\nIf this wasn't you, Change your password and contact customer support\n", "noreply@FriendlyFur.com", to=[old_email])
            sent_email.send()
            messages.success(request, f"Success, Email Confirmation Sent for {new_email}")
            return redirect("/")
    else:
        form = EmailChange()
    return render(request, "authe/email_change.html", context={"form":form})

class CustomLoginView(LoginView):
    template_name = 'authe/login.html'  # Your regular login template
    form_class = AuthenticationForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_after = reverse('login')
            return render(request, 'authe/alreadylogged.html', {'redirect': redirect_after})
        return super().get(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    template_name = 'authe/logout.html'  # Your regular login template

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'authe/notlogged.html')
        return super().get(request, *args, **kwargs)


def email_verification(request, uid64, token):
    id = urlsafe_base64_decode(uid64).decode()
    try:
        id = int(id)
    except:
        messages.error(request, f"Invalid ID. <a href='{reverse('signup')}'>Create Account Again?</a>")
        return redirect("/")
    user = UnverifiedUser.objects.filter(pk=id)
    if not user.exists():
        messages.error(request, f"Account Doesn't exists or expired. <a href='{reverse('signup')}'>Create Account Again?</a>")
        return redirect("/")
    user = user.first()
    if not default_token_generator.check_token(user, token):
        messages.error(request, "Wrong Token")
        return redirect("/")
    if not user.verf_user:
        verified_user = CustomerUser(email=user.email, password=user.password, first_name=user.first_name, middle_name=user.middle_name, last_name=user.last_name)
        #hade el code bt3mil a user w kteer halwe ;)
        verified_user.save()
        if verified_user:
            login(request, verified_user)
            email = EmailMessage(request, f"Account Created",
                                 f"Account created for {verified_user.getfullname()}")
            email.send()
            messages.success(request, f"Account created for {verified_user.getfullname()}")
    else:
        current_user = user.verf_user
        current_user.email = user.email
        current_user.save()
        email = EmailMessage(request, f"Email Changed", f"Email Changed for {current_user.getfullname()}, from {user.email} to {current_user.email}\n\nNot you?! Than please contact our customer support <a href='#'>here</a>")
        email.send()
        messages.success(request, f"Email Changed for {current_user.getfullname()}, from {user.email} to {current_user.email}")
    user.delete()
    return redirect("/")