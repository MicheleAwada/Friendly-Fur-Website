from django import forms

quantity_choices = (
    (i+1,i+1) for i in range(10)
                    )
class add_to_cart(forms.Form):
    quantity = forms.TypedChoiceField(choices=quantity_choices, label="Quantity:")