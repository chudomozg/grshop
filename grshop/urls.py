from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main.views import get_home_page

urlpatterns = [
                  path('', get_home_page, name='home'),
                  path('admin/', admin.site.urls),
                  path('promo/', include(('promo.urls', 'promo'), namespace='promo')),
                  path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
                  path('catalog/', include(('main.urls', 'main'), namespace='catalog')),
                  path('user/', include(('users.urls', 'users'), namespace='users')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
