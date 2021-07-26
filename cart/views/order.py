from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from grshop.settings import ORDER_ALREADY_EXIST_TEXT
from promo.models import Promo
from users.helpers import get_delivery_detail_fields_dict
from ..forms import CheckOutForm
from ..models import Order, OrderItem, Cart
from ..models.order import get_order_hash, create_order


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return orders


@require_POST
def order_add(request):
    checkout_form = CheckOutForm(request.POST or None,
                                 initial=get_delivery_detail_fields_dict(request.user))

    if checkout_form.is_valid():
        print("form data: {}".format(checkout_form.cleaned_data))
        promo = None
        if checkout_form.cleaned_data['promo_code'] \
                and Promo.objects.filter(promo_code=checkout_form.cleaned_data['promo_code']).exists():
            promo = Promo.objects.filter(promo_code=checkout_form.cleaned_data['promo_code'])

        cart = Cart(request)
        order_hash = get_order_hash(cart, promo)
        if Order.objects.filter(order_hash=order_hash).exists():
            # order hash for double check order duplicating
            return render(request,
                          'cart/checkout.html',
                          {'checkout_form': checkout_form,
                           'modal': {
                               'message': ORDER_ALREADY_EXIST_TEXT,
                               'primary_button_text': "Create order",
                               'secondary_button_text': "I don't want"}})

        create_order(user_id=request.user.id,
                     cart=cart,
                     promo=promo,
                     order_hash=order_hash,
                     checkout_form_data=checkout_form.cleaned_data)
        return redirect('users:dashboard')


@login_required(login_url='users:login')
def checkout(request):
    if len(Cart(request)) > 0:
        form = CheckOutForm(request.POST or None,
                            initial=get_delivery_detail_fields_dict(request.user))
        return render(request,
                      'cart/checkout.html',
                      {'checkout_form': form})
    return redirect('cart:cart_detail')
