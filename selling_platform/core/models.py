from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from seats.models import Seat


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])


class TransactionHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(_('amount'))
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    seats = models.ManyToManyField(Seat, related_name='transaction_history', blank=True, null=True)
