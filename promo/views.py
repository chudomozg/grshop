from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from cart.models import Cart
from .forms import CheckPromoCodeForm
from .helpers import is_promocode_exist, get_total_sum_with_promo_discount
from .models import Promo


def promo_list(request):
    # all promos, expired too
    return render(request,
                  'promo/promo_list.html',
                  {'promos': Promo.promo_manager.get_list(show_expired=True)})


def promo_detail(request, promo_slug):
    return render(request,
                  'promo/promo.html',
                  {'promo': get_object_or_404(Promo, slug=promo_slug)})


@require_POST
def check_promocode(request):
    form_check_promocode = CheckPromoCodeForm(request.POST)
    if form_check_promocode.is_valid():
        promocode = form_check_promocode.cleaned_data['promo_code']
        if is_promocode_exist(promocode):
            promo = Promo.objects.get(promo_code=promocode)
            cart = Cart(request)
            if promo.condition(cart):
                total_sum = get_total_sum_with_promo_discount(cart, promo)
                return JsonResponse({'promo': {"title": promo.title,
                                               "discount": promo.discount,
                                               'promo_code': promo.promo_code},
                                     'total_sum': total_sum})
            else:
                message = '''The conditions of the promo code have not been met.
                            Read the conditions of the promotion carefully'''
                return JsonResponse({'modal': {'message': message,
                                               'button': 'Ok'}})
        message = "Promocode doesn't exist"
        return JsonResponse({'modal': {'message': message,
                                       'button': 'Ok'}})
