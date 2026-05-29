from django.urls import path
from .views import CalculateCartView

urlpatterns = [
    path('calculate/', CalculateCartView.as_view(), name='calculate'),
]