from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .forms import UserLoginForm

app_name = 'users'

urlpatterns = [
    path('registration/', views.user_registration, name='registration'),
    path('activate/<slug:uidb64>/<slug:token>', views.user_activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/registration/login.html',
                                                form_class=UserLoginForm,
                                                redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/user/login/'), name='logout'),
    # User dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_details, name='edit_details'),
]