from django.db import models
from decimal import Decimal
from django.conf import settings


class Cart(object):
    def __init__(self, request):
        # cart inicialization
        # if session have cart data - get it, else put empty cart to session
        # cart - dict {key = id of product, value = [count, price]
        # we save price to cart, because price can change.
        # So, we sell the product for the price seen by the buyer at the time of purchase
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save empty cart to session
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, count=1, add_to_count=False):
        # add product into cart or change count
        # we've got to use str(), because Django use JSON for session
        # add_to_count - use for decreasing query "count of products"
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': 0, 'price': str(product.price)}
        if add_to_count:
            self.cart[product_id]['count'] = count
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        # mark session like used
        self.session.modified = True

    def remove(self, product):
        # remove product from cart
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # make generator fog Cart, it will be used for views
        # Work with copy of cart, because we don't need to keep additional info in session
        # Get instances of Product model and put it in cart dict
        # In "yield circle" make price Decimal from str and count total_price for each product
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['count']
        yield item

    def __len__(self):
        # return total sum of all products (product count) in cart
        return sum(item['count'] for item in self.cart.values())

    def get_total_price(self):
        # return total price of all product in cart
        return sum(Decimal(item['price']) * item['count'] for item in self.cart.values())

    def clear(self):
        # clearing of cart - del session
        del self.session[settings.CART_SESSION_ID]
        self.save()