from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    # count product for adding into cart: TypedChoiceField for getting int value automatic
    # def __init__(self, product_stock):
    #     self.product_stock = product_stock

    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                   coerce=int,
                                   widget=forms.Select(attrs={'class': "form-control"}))
