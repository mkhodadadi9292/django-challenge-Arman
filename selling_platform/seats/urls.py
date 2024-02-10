from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('ticket', views.TicketViewSet, basename='ticket')
router.register('stadium', views.StadiumViewSet, basename='stadium')
router.register('seat', views.SeatViewSet, basename='seat')
router.register('match', views.MatchViewSet, basename='match')
router.register('price', views.PriceViewSet, basename='price')

urlpatterns = [
    path('', include(router.urls))
]
