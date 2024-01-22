from django.contrib import admin
from .models import Ticket, Seat, Stadium, Price, Match

# Register your model with the admin site
admin.site.register(Ticket)
admin.site.register(Seat)
admin.site.register(Price)
admin.site.register(Stadium)
admin.site.register(Match)
