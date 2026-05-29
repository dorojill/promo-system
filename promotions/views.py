from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from .models import Promotion
from .serializers import PromotionSerializer


# ---- REST API ----

class PromotionListCreateView(generics.ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class PromotionDetailView(generics.RetrieveUpdateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


class ActivatePromotionView(APIView):
    def post(self, request, pk):
        try:
            promotion = Promotion.objects.get(pk=pk)
            promotion.status = 'ACTIVE'
            promotion.save()
            return Response({'status': 'активирована'})
        except Promotion.DoesNotExist:
            return Response(
                {'error': 'не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeactivatePromotionView(APIView):
    def post(self, request, pk):
        try:
            promotion = Promotion.objects.get(pk=pk)
            promotion.status = 'PAUSED'
            promotion.save()
            return Response({'status': 'приостановлена'})
        except Promotion.DoesNotExist:
            return Response(
                {'error': 'не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )


# ---- HTML страницы ----

def promotion_list_view(request):
    queryset = Promotion.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status')
    promo_type = request.GET.get('promo_type')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if promo_type:
        queryset = queryset.filter(promo_type=promo_type)
    return render(request, 'promotion_list.html',
                  {'promotions': queryset})


def promotion_detail_view(request, pk):
    promo = get_object_or_404(Promotion, pk=pk)
    return render(request, 'promotion_detail.html', {'promo': promo})


def promotion_activate_view(request, pk):
    promo = get_object_or_404(Promotion, pk=pk)
    promo.status = 'ACTIVE'
    promo.save()
    django_messages.success(
        request, f'Акция «{promo.name}» активирована'
    )
    return redirect('promotion_list')


def promotion_deactivate_view(request, pk):
    promo = get_object_or_404(Promotion, pk=pk)
    promo.status = 'PAUSED'
    promo.save()
    django_messages.warning(
        request, f'Акция «{promo.name}» приостановлена'
    )
    return redirect('promotion_list')


def promotion_create_view(request):
    return render(request, 'promotion_create.html')