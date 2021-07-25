from django.utils.encoding import force_bytes, force_text

from .forms import RegistrationForm
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token


def user_registration(request):
    if request.user.is_authenticated:
        return redirect('user:dashboard')

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
                'user/registration/account_act_email.html',
                {
                    'user': user,
                    'domain': domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject="Please Activate your Account on {}".format(domain),
                            message=message)
            success_text = '''Your registration was successful.
                            You need to activate your account for use on the site. 
                            An email was sent to you with an activation link and further instructions.'''
            return render(request, 'user/registration/register.html', {'form': reg_form,
                                                                       'modal': {
                                                                           'message': success_text,
                                                                           'button_text': "Understood"
                                                                       }})
    else:
        reg_form = RegistrationForm()
    return render(request, 'user/registration/register.html', {'form': reg_form})