from django.shortcuts import render,redirect, reverse
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, authenticate

def signup(request):
    redirect_after = reverse('signup')
    if request.user.is_authenticated:
        return render(request, "authe/alreadylogged.html", {'redirect': redirect_after})
    if request.method=="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data.get("full_name")
            name_words = full_name.split()
            first_name = name_words.pop(-1)
            last_name = name_words.pop(-1)
            middle_name = None
            if name_words:
                middle_name = " ".join(name_words)
            form.save()

            authenticated_user = authenticate(first_name=first_name, last_name=last_name, middle_name=middle_name,username=form.cleaned_data.get("email"), password=form.cleaned_data.get('password1'))
            if authenticated_user:
                login(request, authenticated_user)
                messages.success(request, f"Account created for {full_name}")
                return redirect('home')
            else:
                messages.error('Something went wrong during authentication.')
    else:
        form = UserRegisterForm()
    form.fields['full_name'].label = "Full Name"
    return render(request, "authe/signup.html", {'form': form})


def account(request):
    if request.user.is_authenticated:
        user = request.user
        info = [user.email, user.first_name, user.middle_name, user.last_name]
        return render(request, "registration/temp remove.html", {"info": info})
    return redirect(reverse('login'))


class CustomLoginView(LoginView):
    template_name = 'authe/login.html'  # Your regular login template

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