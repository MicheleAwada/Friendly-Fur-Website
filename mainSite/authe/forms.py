from django import forms
from .models import CustomerUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(label="Full_Name", required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomerUser
        fields = ['full_name','email','password1','password2']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        words = full_name.split()

        if len(words) < 2:
            raise forms.ValidationError("Please enter a full name with at least two words.")

        return full_name

class AllergyAutocompleteForm(forms.Form):
    allergy = forms.CharField(max_length=1000, required=False)
    name = forms.CharField(max_length=100, required=False)
    breed = forms.CharField(max_length=100, required=False)