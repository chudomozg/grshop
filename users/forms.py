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