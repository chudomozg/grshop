from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('activate/<slug:uidb64>/<slug:token>', views.user_activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/registration/login.html'),name='login')
                                                # form_class=UserLoginForm), name='login'),
]