from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.mail import send_mail

from grshop.settings import DEFAULT_FROM_EMAIL, EMAIL_BACKEND, SENDING_EMAIL_OFF


class CustomUserManager(BaseUserManager):
    # custom manager for UserBase extended BaseUserManager
    # BaseUserManager class of Django for Manage Users
    # Added some custom validation for creation superuser and normal user

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    # Delivery details
    country = models.CharField(max_length=20, blank=True)
    area = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=12, blank=True)

    # User Status:
    # In default user will not active
    # It will be activate after email confirming
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def email_user(self, subject, message):
        # Method for sending email
        # check settings.py for setup
        # if you use app in dev server, just check console
        # all emails, that have to be send will be shown in console
        if SENDING_EMAIL_OFF:
            print ('''YOU HAVE TRIED TO SEND EMAIL FROM GRSHOP WITH SENDING_EMAIL_OFF=TRUE
                    Subject: {}
                    Message: {}
                    FOR SENDING EMAIL FROM PRODUCT CHECK SETTINGS.PY'''.format(subject, message))
        else:
            send_mail(
                subject,
                message,
                DEFAULT_FROM_EMAIL,
                [self.email],
                fail_silently=False,
                connection=EMAIL_BACKEND
            )

    def __str__(self):
        return self.user_name
