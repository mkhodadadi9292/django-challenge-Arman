from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


# from

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)