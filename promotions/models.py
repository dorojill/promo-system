from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import Product, Category

User = get_user_model()


class Promotion(models.Model):
    PROMO_TYPE_CHOICES = [
        ('PERCENT', 'Процентная скидка'),
        ('FIXED', 'Фиксированная скидка'),
        ('N_PLUS_1', 'N+1 (бесплатный товар)'),
        ('THRESHOLD', 'Пороговая скидка'),
        ('BUNDLE', 'Бандл'),
    ]

    STATUS_CHOICES = [
        ('DRAFT', 'Черновик'),
        ('SCHEDULED', 'Запланирована'),
        ('ACTIVE', 'Активна'),
        ('PAUSED', 'Приостановлена'),
        ('COMPLETED', 'Завершена'),
    ]

    name = models.CharField(
        max_length=300,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    promo_type = models.CharField(
        max_length=50,
        choices=PROMO_TYPE_CHOICES,
        verbose_name='Тип акции'
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Размер скидки'
    )
    threshold_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Пороговая сумма'
    )
    n_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Количество N'
    )
    plus_quantity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Бесплатных единиц'
    )
    priority = models.IntegerField(
        default=0,
        verbose_name='Приоритет'
    )
    is_combinable = models.BooleanField(
        default=False,
        verbose_name='Совместима с другими акциями'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        verbose_name='Статус'
    )
    start_datetime = models.DateTimeField(
        verbose_name='Начало действия'
    )
    end_datetime = models.DateTimeField(
        verbose_name='Конец действия'
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        through='PromotionProduct',
        verbose_name='Товары'
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        through='PromotionCategory',
        verbose_name='Категории'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_promotions',
        verbose_name='Создал'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        indexes = [
            models.Index(
                fields=['status', 'start_datetime', 'end_datetime']
            ),
        ]

    def __str__(self):
        return self.name


class PromotionProduct(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        verbose_name='Акция'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )

    class Meta:
        verbose_name = 'Товар акции'
        verbose_name_plural = 'Товары акции'
        unique_together = ('promotion', 'product')

    def __str__(self):
        return f'{self.promotion} — {self.product}'


class PromotionCategory(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        verbose_name='Акция'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Категория акции'
        verbose_name_plural = 'Категории акции'
        unique_together = ('promotion', 'category')

    def __str__(self):
        return f'{self.promotion} — {self.category}'


class PromotionApplication(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        null=True,
        related_name='applications',
        verbose_name='Акция'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Товар'
    )
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время применения'
    )
    original_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Базовая цена'
    )
    final_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Итоговая цена'
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма скидки'
    )
    session_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='ID сессии'
    )

    class Meta:
        verbose_name = 'Применение акции'
        verbose_name_plural = 'Применения акций'
        indexes = [
            models.Index(fields=['promotion', 'applied_at']),
        ]

    def __str__(self):
        return f'{self.promotion} — {self.product} — {self.applied_at}'


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Создание'),
        ('UPDATE', 'Изменение'),
        ('DELETE', 'Удаление'),
        ('ACTIVATE', 'Активация'),
        ('DEACTIVATE', 'Деактивация'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Пользователь'
    )
    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        verbose_name='Действие'
    )
    entity_type = models.CharField(
        max_length=50,
        verbose_name='Тип объекта'
    )
    entity_id = models.IntegerField(
        verbose_name='ID объекта'
    )
    changed_fields = models.TextField(
        blank=True,
        verbose_name='Изменённые поля'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время'
    )

    class Meta:
        verbose_name = 'Запись журнала'
        verbose_name_plural = 'Журнал изменений'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action} — {self.entity_type} #{self.entity_id}'