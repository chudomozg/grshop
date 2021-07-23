from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 100)]

class CartAddProductForm(forms.Form):
    # count product for adding into cart: TypedChoiceField for getting int value automatic
    # add bool : True - add, False - replace
    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    add = forms.BooleanField(required=False,
                             initial=False,
                             widget=forms.HiddenInput)
