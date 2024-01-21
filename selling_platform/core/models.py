from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models


# from

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.IntegerField(_('money'), default=1000)


class FinancialStatement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(_('amount'))
    user = models.ForeignKey(User, on_delete=models.PROTECT)
