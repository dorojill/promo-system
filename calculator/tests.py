from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from catalog.models import Category, Product
from promotions.models import Promotion, PromotionProduct
from calculator.services import DiscountService

User = get_user_model()


class DiscountServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.category = Category.objects.create(name='Напитки')
        self.product = Product.objects.create(
            sku='TEST001',
            name='Сок апельсиновый 1л',
            category=self.category,
            base_price=Decimal('89.90'),
            unit='pcs',
        )
        self.now = timezone.now()
        self.service = DiscountService()

    def _create_promotion(self, promo_type, discount_value=None, **kwargs):
        promo = Promotion.objects.create(
            name=f'Тест {promo_type}',
            promo_type=promo_type,
            discount_value=discount_value,
            status='ACTIVE',
            start_datetime=self.now - timedelta(hours=1),
            end_datetime=self.now + timedelta(hours=1),
            created_by=self.user,
            priority=1,
            **kwargs
        )
        PromotionProduct.objects.create(
            promotion=promo, product=self.product
        )
        return promo

    def test_percent_discount(self):
        self._create_promotion('PERCENT', discount_value=Decimal('10'))
        result = self.service.calculate_cart(
            [{'product_id': self.product.id, 'quantity': 1}]
        )
        expected = Decimal('80.91')
        self.assertEqual(
            Decimal(result['items'][0]['final_price']), expected
        )

    def test_fixed_discount(self):
        self._create_promotion('FIXED', discount_value=Decimal('20'))
        result = self.service.calculate_cart(
            [{'product_id': self.product.id, 'quantity': 1}]
        )
        expected = Decimal('69.90')
        self.assertEqual(
            Decimal(result['items'][0]['final_price']), expected
        )

    def test_n_plus_1_discount(self):
        self._create_promotion(
            'N_PLUS_1',
            n_quantity=2,
            plus_quantity=1
        )
        result = self.service.calculate_cart(
            [{'product_id': self.product.id, 'quantity': 3}]
        )
        line_total = Decimal(result['items'][0]['line_total'])
        expected_total = (self.product.base_price * 2).quantize(
            Decimal('0.01')
        )
        self.assertEqual(
            line_total.quantize(Decimal('0.01')), expected_total
        )

    def test_no_promotion(self):
        result = self.service.calculate_cart(
            [{'product_id': self.product.id, 'quantity': 2}]
        )
        self.assertIsNone(result['items'][0]['promotion'])
        self.assertEqual(
            result['items'][0]['final_price'],
            str(self.product.base_price)
        )

    def test_priority_selection(self):
        self._create_promotion(
            'PERCENT', discount_value=Decimal('5'), priority=1
        )
        promo2 = self._create_promotion(
            'PERCENT', discount_value=Decimal('15'), priority=5
        )
        result = self.service.calculate_cart(
            [{'product_id': self.product.id, 'quantity': 1}]
        )
        self.assertEqual(result['items'][0]['promotion'], promo2.name)