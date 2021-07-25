from django import forms
from .models import UserBase


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label="Username",
                                min_length=5,
                                max_length=20,
                                help_text="Required")
    email = forms.EmailField(label="Email",
                             max_length=50,
                             help_text="Required")
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput,
                               min_length=6)
    password2 = forms.CharField(label="Repeat password",
                                widget=forms.PasswordInput,
                                min_length=6)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_username(self):
        # validation for username
        # if username already exist then raise error
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        # validation for password
        # compare pass1 and pass2
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        # validation for email
        # if email already exist then raise error
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
