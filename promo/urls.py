from django.urls import path
from . import views

urlpatterns = [
    path('', views.promo_list, name='promo_list'),
    path('<promo_slug>/', views.promo_detail, name='promo_detail'),
    path('check_promocode', views.check_promocode, name='check_promocode')
]