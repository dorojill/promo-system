from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import DiscountService
from .serializers import CartInputSerializer
import uuid


class CalculateCartView(APIView):

    def post(self, request):
        serializer = CartInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        service = DiscountService()
        session_id = str(uuid.uuid4())
        result = service.calculate_cart(
            items=serializer.validated_data['items'],
            session_id=session_id
        )
        return Response(result, status=status.HTTP_200_OK)