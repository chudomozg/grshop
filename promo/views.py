from django.shortcuts import render, get_object_or_404
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
