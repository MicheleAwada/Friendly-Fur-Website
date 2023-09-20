from django import forms
from .models import CustomerUser, CustomerDog, PossibleAllergies, PossibleBreeds, UnverifiedUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
import json
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password

class EmailChange(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EmailChange, self).__init__(*args, **kwargs)

    email = forms.EmailField(label="New Email")
    password = forms.CharField(label="Account Password",widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomerUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already Taken")
        return email
    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user:
            raise forms.ValidationError("You Must have a User")
        if not self.user.check_password(self.cleaned_data.get("password")):
            raise forms.ValidationError("Password isn't correct")
        return "Pass"
    def save(self, commit=True):
        if self.user:
            unverf_user = super(EmailChange, self).save(commit=False)
            unverf_user.verf_user = self.user

            if commit:
                unverf_user.save()
            return unverf_user
        else:
            raise forms.ValidationError("Incorrect Password")
    class Meta:
        model = UnverifiedUser
        fields = ['email', "password"]

class CustomerDogForm(forms.ModelForm):

    genders = [
        ("m","Male"),
        ("f","Female")
    ]
    name = forms.CharField(required=True)
    breed = forms.CharField(required=False)
    allergys = forms.CharField(required=False)
    age = forms.IntegerField(
        validators=[
            MinValueValidator(limit_value=0),  # Set the minimum value
            MaxValueValidator(limit_value=32)  # Set the maximum value
        ],
        required=False
    )
    gender = forms.ChoiceField(choices=genders)
    allergys_hidden = forms.CharField(required=False)
    breed_hidden = forms.CharField(required=False)

    class Meta:
        model = CustomerDog
        fields = ["name", "breed_hidden", "breed", "allergys_hidden", "allergys", "age", "gender"]

    def clean_allergys(self):# no clean_allergys_hidden sincee its not shown so errors wont be shown
        allergys = self.cleaned_data.get("allergys_hidden")
        breeds = self.cleaned_data.get("breed_hidden")
        if allergys:
            try:
                allergys = json.loads(allergys)
            except:
                raise forms.ValidationError("Error with verifying allergies")
            for allergy in allergys:
                if not PossibleAllergies.objects.filter(name=allergy).exists():
                    raise forms.ValidationError("Error, allergy doesnt exist")
        if breeds:
            try:
                breeds = json.loads(breeds)
            except:
                raise forms.ValidationError("Error with verifying breeds")
            for breed in breeds:
                if not PossibleBreeds.objects.filter(name=breed).exists():
                    raise forms.ValidationError("Error, breed doesnt exist")
        return ""

    def save(self, request, commit=True):
        dog = super(CustomerDogForm, self).save(commit=False)
        dog.is_male = True if self.cleaned_data['gender']=="m" else False

        dog.human = request.user
        if commit:
            dog.save()
            allergies_data = self.cleaned_data.get("allergys_hidden")
            breeds_data = self.cleaned_data.get("breed_hidden")
            if allergies_data:
                allergies_data = json.loads(allergies_data)
                allergys_query_set = PossibleAllergies.objects.filter(name__in=allergies_data)
                dog.allergys.add(*allergys_query_set)
            if breeds_data:
                breeds_data = json.loads(breeds_data)
                breeds_query_set = PossibleBreeds.objects.filter(name__in=breeds_data)
                dog.breed.add(*breeds_query_set)
        return dog





def is_full_name_valid(full_name):
    words = full_name.split()

    if len(words) < 2:
        raise forms.ValidationError("Please enter a full name with at least two words.")
def get_names_from_fullname(full_name):
    name_words = full_name.split()
    first_name = name_words.pop(0)
    last_name = name_words.pop(-1)
    middle_name = None
    if name_words:
        middle_name = " ".join(name_words)
    return [first_name, middle_name, last_name]

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(label="Full Name", required=True, max_length=60)
    email = forms.EmailField(required=True)
    class Meta:
        model = UnverifiedUser
        fields = ['full_name','email','password1','password2']
    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        is_full_name_valid(full_name)
        first_name, middle_name, last_name = get_names_from_fullname(full_name=full_name)
        self.cleaned_data['first_name'] = first_name
        self.cleaned_data['middle_name'] = middle_name
        self.cleaned_data['last_name'] = last_name
        return full_name
    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomerUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Taken")
        return email
    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user
class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(label="Full Name", required=True)

    class Meta:
        model = CustomerUser
        fields = ['full_name','email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        verified, _ = Group.get_or_create(name="verified")
        if verified.user_set.filter(email=email).exists():
            raise forms.ValidationError("Email Is in Use")

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class AllergyAutocompleteForm(forms.Form):
    allergy = forms.CharField(max_length=1000, required=False)
    name = forms.CharField(max_length=100, required=False)
    breed = forms.CharField(max_length=100, required=False)