from rest_framework import serializers
from .models import Promotion, PromotionProduct, PromotionCategory


class PromotionSerializer(serializers.ModelSerializer):
    product_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Promotion
        fields = [
            'id', 'name', 'description', 'promo_type',
            'discount_value', 'threshold_amount',
            'n_quantity', 'plus_quantity', 'priority',
            'is_combinable', 'status',
            'start_datetime', 'end_datetime',
            'product_ids', 'category_ids',
            'created_at', 'updated_at'
        ]

    def create(self, validated_data):
        product_ids = validated_data.pop('product_ids', [])
        category_ids = validated_data.pop('category_ids', [])
        promotion = Promotion.objects.create(**validated_data)
        for pid in product_ids:
            PromotionProduct.objects.create(
                promotion=promotion, product_id=pid
            )
        for cid in category_ids:
            PromotionCategory.objects.create(
                promotion=promotion, category_id=cid
            )
        return promotion