from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'main/catalog/catalog.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def get_home_page(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, on_front=True)
    return render(request,
                  'main/home.html',
                  {'categories': categories,
                   'products': products})


def product_detail(request, product_slug, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    return render(request,
                  'main/catalog/product.html',
                  {'product': get_object_or_404(Product,
                                                slug=product_slug,
                                                available=True),
                   'category': category,
                   'ancestors': category.get_ancestors(include_self=True),
                   'cart_product_form': CartAddProductForm()})
