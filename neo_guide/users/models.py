from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=False, blank=True)
    email = models.EmailField(_('Adres e-mail'), unique=True)
    first_name = models.CharField(_('Imię'), max_length=100, blank=True)
    last_name = models.CharField(_('Nazwisko'), max_length=100, blank=True)
    city = models.CharField(_('Miasto'), max_length=100, blank=True)
    parish = models.CharField(_('Parafia'), max_length=100, blank=True)
    community = models.CharField(_('Wspólnota'), max_length=100, blank=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'User {self.email}'
