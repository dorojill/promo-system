from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta


def analytics_view(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    return render(request, 'analytics.html', {
        'date_from': str(week_ago),
        'date_to': str(today),
    })


def analytics_api_view(request):
    from django.http import JsonResponse
    from promotions.models import PromotionApplication, Promotion
    from django.db.models import Count, Sum
    from datetime import datetime

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    apps = PromotionApplication.objects.all()
    if date_from:
        apps = apps.filter(applied_at__date__gte=date_from)
    if date_to:
        apps = apps.filter(applied_at__date__lte=date_to)

    # По дням
    from django.db.models.functions import TruncDate
    daily = list(
        apps.annotate(date=TruncDate('applied_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )
    daily_data = [
        {'date': str(d['date']), 'count': d['count']}
        for d in daily
    ]

    # По типам
    type_labels = {
        'PERCENT': 'Процентная',
        'FIXED': 'Фиксированная',
        'N_PLUS_1': 'N+1',
        'THRESHOLD': 'Пороговая',
        'BUNDLE': 'Бандл',
    }
    by_type_qs = (
        apps.values('promotion__promo_type')
        .annotate(total=Sum('discount_amount'))
    )
    by_type = [
        {
            'label': type_labels.get(
                item['promotion__promo_type'], item['promotion__promo_type']
            ),
            'total': float(item['total'] or 0),
        }
        for item in by_type_qs
    ]

    # По акциям
    by_promo = list(
        apps.values('promotion__name')
        .annotate(count=Count('id'), total_discount=Sum('discount_amount'))
        .order_by('-count')
    )
    by_promo_data = [
        {
            'name': item['promotion__name'] or 'Удалена',
            'count': item['count'],
            'total_discount': float(item['total_discount'] or 0),
        }
        for item in by_promo
    ]

    return JsonResponse({
        'daily': daily_data,
        'by_type': by_type,
        'by_promotion': by_promo_data,
    })