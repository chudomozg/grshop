from .models.promo import get_promos_list


def promos(request):
    return {'promos': get_promos_list()}
