from promo.models import Promo
from decimal import Decimal
from datetime import datetime, timedelta


def get_total_sum_with_promo_discount(cart, promo):
    return round(cart.get_total_price() * Decimal(1 - promo.discount / 100), 2)


def is_promocode_exist(promocode):
    if Promo.objects.filter(promo_code=promocode, end_date__gte=datetime.today()).count():
        return True
    return False
