from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Stadium(models.Model):
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.description}"


class Seat(models.Model):
    seat_number = models.IntegerField()
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.seat_number=}_{self.stadium.description}"


class Match(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # stadium = models.ManyToManyField(Stadium, related_name='match', blank=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)


class Price(models.Model):
    name = models.CharField(max_length=20)
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
    price = models.ForeignKey(
        Price, on_delete=models.CASCADE)
    status = models.IntegerField(
        max_length=1, choices=SEAT_STATUS, default=EMPTY)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    stadium = models.ForeignKey(Stadium, on_delete=models.PROTECT)
