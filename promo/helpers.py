def get_total_sum_with_promo_discount(cart, promo):
    return round(cart.get_total_price() * (1 - promo.discount / 100), 2)