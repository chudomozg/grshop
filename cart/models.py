from django.db import models
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from main.models import Product


class Cart(object):
    def __init__(self, request):
        # cart initialization
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

    def add(self, product_id, count=1):
        # add product into cart or change count
        # we've got to use str(), because Django use JSON for session
        product = get_object_or_404(Product, id=product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': count, 'price': str(product.price)}
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        # mark session like used
        self.session.modified = True

    def remove(self, product_id):
        # remove product from cart
        # product_id = str(product.id)
        if Product.objects.filter(id=product_id).exists():
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
            cart[product.id]['product'] = product

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
