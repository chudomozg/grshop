from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from users.helpers import get_delivery_detail_fields_dict
from ..forms import CheckOutForm
from ..models import Order, OrderItem, Cart


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return orders


@login_required(login_url='users:login')
def checkout(request):
    form = CheckOutForm(request.POST or None,
                        initial=get_delivery_detail_fields_dict(request.user))
    return render(request,
                  'cart/checkout.html',
                  {'checkout_form': form})
