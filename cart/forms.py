from django import forms
from django.forms import Select

from cart.models import Order
from grshop.settings import DELIVERY_TYPE, BILLING_TYPE, AVAILABLE_BILLING_TYPE, AVAILABLE_DELIVERY_TYPE

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CartAddProductForm(forms.Form):
    # count product for adding into cart: TypedChoiceField for getting int value automatic
    # def __init__(self, product_stock):
    #     self.product_stock = product_stock

    count = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                   coerce=int,
                                   widget=forms.Select(attrs={'class': "form-control"}))


class SelectWidgetWithDisableOptions(Select):
    # Subclass of Django's select widget that allows disabling options.

    def __init__(self, disabled_choices=[], *args, **kwargs):
        self._disabled_choices = disabled_choices
        super(SelectWidgetWithDisableOptions, self).__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super(SelectWidgetWithDisableOptions, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict


class CheckOutForm(forms.Form):
    promo_code = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'value': 'special'}))
    first_name = forms.CharField(required=True, )
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    country = forms.CharField(required=True)
    area = forms.CharField(required=True)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    postcode = forms.CharField(required=True)
    billing_type = forms.ChoiceField(choices=BILLING_TYPE.items(),
                                     widget=SelectWidgetWithDisableOptions(disabled_choices=AVAILABLE_BILLING_TYPE))
    delivery_type = forms.ChoiceField(choices=DELIVERY_TYPE.items(),
                                      widget=SelectWidgetWithDisableOptions(disabled_choices=AVAILABLE_DELIVERY_TYPE))
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 5, "cols": 20}), required=False)

    class Meta:
        model = Order
        fields = (
            'promo_code'
            'first_name',
            'last_name',
            'phone_number',
            'country',
            'area',
            'city',
            'address',
            'postcode',
            'billing_type',
            'delivery_type',
            'comment'
        )
