from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import login, logout

from cart.views import user_orders
from grshop.settings import REGISTRATION_SUCCESS_TEXT
from .forms import RegistrationForm, UserEditForm
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import UserBase
from .tokens import user_activation_token


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('users:dashboard')

    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.email = reg_form.cleaned_data['email']
            user.set_password(reg_form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # setup Email
            domain = get_current_site(request).domain
            message = render_to_string(
                'users/registration/account_act_email.html',
                {
                    'user': user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': user_activation_token.make_token(user),
                })
            user.email_user(subject="Please Activate your Account on {}".format(domain),
                            message=message)
            return render(request, 'users/registration/register.html', {'form': reg_form,
                                                                        'modal': {
                                                                            'message': REGISTRATION_SUCCESS_TEXT,
                                                                            'button_text': "Understood"}})
    else:
        reg_form = RegistrationForm()
    return render(request, 'users/registration/register.html', {'form': reg_form})


def user_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and user_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('users:dashboard')
    else:
        return render(request, 'users/registration/activation_invalid.html')


@login_required(login_url='users:login')
def dashboard(request):
    orders = user_orders(request)
    return render(request,
                  'users/user/dashboard.html',
                  {'orders': orders})


@login_required(login_url='users:login')
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'users/user/edit_details.html', {'user_form': user_form})
