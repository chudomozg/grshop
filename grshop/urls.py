from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main.views import promo_detail, promo_list, get_home_page

urlpatterns = [
                  path('', get_home_page, name='home'),
                  path('admin/', admin.site.urls),
                  path('promo/<promo_slug>', promo_detail, name='promo_detail'),
                  path('promo/', promo_list, name='promo_list'),
                  path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
                  path('catalog/', include(('main.urls', 'main'), namespace='catalog')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
