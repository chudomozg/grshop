from .models import Promo


def promos(request):
    return {'promos': Promo.promo_manager.get_list()}
