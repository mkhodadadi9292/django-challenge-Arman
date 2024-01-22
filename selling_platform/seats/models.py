from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Price(models.Model):
    name = models.CharField(max_length=10)
    unit_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)])


class Ticket(models.Model):
    RESERVED = 1
    CANCELLED = 2
    CONFIRMED = 3
    EMPTY = 4
    EXPIRED = 5

    SEAT_STATUS = [
        (RESERVED, 'RESERVED'),
        (CANCELLED, 'CANCELLED'),
        (CONFIRMED, 'CONFIRMED'),
        (EMPTY, 'EMPTY'),
        (EXPIRED, 'EXPIRED')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    # type = models.SmallIntegerField(null=False)
    price = models.ForeignKey(
        Price, on_delete=models.CASCADE)
    status = models.IntegerField(
        max_length=1, choices=SEAT_STATUS, default=EMPTY)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)