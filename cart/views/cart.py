from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from main.models import Product
from ..models import Cart
from ..forms import CartAddProductForm
from django.http import JsonResponse


@require_POST
def cart_add(request, product_id):
    # we will use this view only in POST request.
    # So we need to process the form data:
    # after processing we add data to cart
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product_id=product_id,
                 count=cd['count'])
    # return redirect('cart:cart_detail')
    response = JsonResponse({'count': cart.__len__()})
    return response


def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart:cart_detail')


def cart_detail(request):
    return render(request, 'cart/detail.html', {'cart': Cart(request)})
