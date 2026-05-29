from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Promotion
from .serializers import PromotionSerializer


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