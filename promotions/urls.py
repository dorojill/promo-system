from django.urls import path
from . import views

urlpatterns = [
    path(
        'promotions/',
        views.PromotionListCreateView.as_view(),
        name='promotion-list'
    ),
    path(
        'promotions/<int:pk>/',
        views.PromotionDetailView.as_view(),
        name='promotion-detail'
    ),
    path(
        'promotions/<int:pk>/activate/',
        views.ActivatePromotionView.as_view(),
        name='promotion-activate'
    ),
    path(
        'promotions/<int:pk>/deactivate/',
        views.DeactivatePromotionView.as_view(),
        name='promotion-deactivate'
    ),
]