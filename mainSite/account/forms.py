from django import forms
from authe.forms import get_names_from_fullname, is_full_name_valid
from authe.models import CustomerUser
from django.http import HttpResponseServerError

class changeName(forms.ModelForm):

    full_name = forms.CharField(max_length=90)

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        is_full_name_valid(full_name)
        first_name, middle_name, last_name = get_names_from_fullname(full_name=full_name)
        if first_name == self.instance.first_name and middle_name == self.instance.middle_name and last_name == self.instance.last_name:
            raise forms.ValidationError("You didn't change your name")
        self.cleaned_data['first_name'] = first_name
        self.cleaned_data['middle_name'] = middle_name
        self.cleaned_data['last_name'] = last_name
        return full_name

    def save(self, commit=True):
        if not self.instance:
            raise HttpResponseServerError
        user = super(changeName, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_name = self.cleaned_data['middle_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user
    class Meta:
        model = CustomerUser
        fields = ["full_name"]