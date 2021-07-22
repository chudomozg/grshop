from django import forms
from grshop.settings import PRODUCT_QUANTITY_CHOICES


class CartAddProductForm(forms.Form):
    # count product for adding into cart: TypedChoiceField for getting int value automatic
    # add bool : True - add, False - replace
    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    add = forms.BooleanField(required=False,
                             initial=False,
                             widget=forms.HiddenInput)
