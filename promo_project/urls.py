from django.contrib import admin
from django.urls import path, include
from . import views as project_views
from promotions import views as promo_views
from catalog import views as catalog_views
from calculator.views_html import calculator_view
from analytics.views import analytics_view, analytics_api_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Страницы
    path('', project_views.dashboard_view, name='dashboard'),
    path('promotions/', promo_views.promotion_list_view,
         name='promotion_list'),
    path('promotions/<int:pk>/', promo_views.promotion_detail_view,
         name='promotion_detail'),
    path('promotions/create/', promo_views.promotion_create_view,
         name='promotion_create'),
    path('promotions/<int:pk>/activate/',
         promo_views.promotion_activate_view, name='promotion_activate'),
    path('promotions/<int:pk>/deactivate/',
         promo_views.promotion_deactivate_view,
         name='promotion_deactivate'),
    path('products/', catalog_views.product_list_view, name='product_list'),
    path('calculator/', calculator_view, name='calculator'),
    path('analytics/', analytics_view, name='analytics'),

    # API
    path('api/', include('catalog.urls')),
    path('api/', include('calculator.urls')),
    path('api/', include('promotions.urls')),
    path('api/analytics/', analytics_api_view, name='analytics_api'),
]