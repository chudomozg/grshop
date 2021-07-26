from django import forms


class CheckPromoCodeForm(forms.Form):
    promo_code = forms.CharField(required=True)
