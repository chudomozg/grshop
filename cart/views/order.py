from django.shortcuts import render
from ..models import Order, OrderItem


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id)
    return orders
