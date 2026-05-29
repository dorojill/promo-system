from decimal import Decimal
from django.utils import timezone
from catalog.models import Product
from promotions.models import Promotion, PromotionApplication


class DiscountService:

    def get_active_promotions(self):
        now = timezone.now()
        return list(
            Promotion.objects.filter(
                status='ACTIVE',
                start_datetime__lte=now,
                end_datetime__gte=now
            ).prefetch_related('products', 'categories')
        )

    def calculate_cart(self, items, session_id=''):
        promotions = self.get_active_promotions()
        result_items = []
        total_original = Decimal('0')
        total_final = Decimal('0')
        total_discount = Decimal('0')

        for item in items:
            try:
                product = Product.objects.get(
                    id=item['product_id'],
                    is_active=True
                )
            except Product.DoesNotExist:
                continue

            quantity = int(item.get('quantity', 1))
            original_price = product.base_price
            applicable = self._find_applicable(product, promotions)

            if applicable:
                best = max(applicable, key=lambda p: p.priority)
                final_price = self._apply(best, original_price, quantity)
                discount = (original_price - final_price) * quantity
                PromotionApplication.objects.create(
                    promotion=best,
                    product=product,
                    original_price=original_price,
                    final_price=final_price,
                    discount_amount=discount,
                    session_id=session_id,
                )
            else:
                final_price = original_price
                discount = Decimal('0')
                best = None

            line_final = final_price * quantity
            line_original = original_price * quantity

            result_items.append({
                'product_id': product.id,
                'sku': product.sku,
                'name': product.name,
                'quantity': quantity,
                'original_price': str(original_price),
                'final_price': str(final_price),
                'discount': str(original_price - final_price),
                'line_total': str(line_final),
                'promotion': best.name if best else None,
            })

            total_original += line_original
            total_final += line_final
            total_discount += discount

        return {
            'items': result_items,
            'total_original': str(total_original),
            'total_final': str(total_final),
            'total_discount': str(total_discount),
        }

    def _find_applicable(self, product, promotions):
        applicable = []
        for promo in promotions:
            product_ids = [p.id for p in promo.products.all()]
            category_ids = [c.id for c in promo.categories.all()]
            if (product.id in product_ids
                    or product.category_id in category_ids):
                applicable.append(promo)
        return applicable

    def _apply(self, promotion, base_price, quantity):
        ptype = promotion.promo_type

        if ptype == 'PERCENT':
            rate = promotion.discount_value / Decimal('100')
            return (base_price * (1 - rate)).quantize(Decimal('0.01'))

        elif ptype == 'FIXED':
            return max(
                base_price - promotion.discount_value,
                Decimal('0')
            ).quantize(Decimal('0.01'))

        elif ptype == 'N_PLUS_1':
            n = promotion.n_quantity or 1
            plus = promotion.plus_quantity or 1
            total_units = n + plus
            if quantity >= total_units:
                paid = quantity - (quantity // total_units) * plus
                return (base_price * paid / quantity).quantize(
                    Decimal('0.01')
                )
            return base_price

        return base_price