from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class Feeds(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200, blank=False, default='')
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title

class UserProfileManager(BaseUserManager):


    def create_user(self,email,username,image,password=None):

        if not email:
            raise ValueError('User must have an email address')

        email=self.normalize_email(email)
        user=self.model(email=email,username=username,image=image)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,username,image,password):

        user=self.create_user(email,username,image,password)

        user.is_superuser=True
        user.is_staff=True

        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):


    image = models.ImageField(null=True, blank=True)
    email=models.EmailField(max_length=255,unique=True)
    username=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(null=True, blank=True)

    object=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','image']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
