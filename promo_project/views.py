from django.shortcuts import render
from promotions.models import Promotion
from catalog.models import Product


def dashboard_view(request):
    return render(request, 'dashboard.html', {
        'active_count': Promotion.objects.filter(status='ACTIVE').count(),
        'scheduled_count': Promotion.objects.filter(
            status='SCHEDULED'
        ).count(),
        'completed_count': Promotion.objects.filter(
            status='COMPLETED'
        ).count(),
        'product_count': Product.objects.filter(is_active=True).count(),
        'active_promotions': Promotion.objects.filter(
            status='ACTIVE'
        ).order_by('-priority')[:10],
    })