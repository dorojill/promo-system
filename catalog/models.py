from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('pcs', 'шт.'),
        ('kg', 'кг'),
        ('l', 'л'),
        ('m', 'м'),
    ]

    sku = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Артикул'
    )
    name = models.CharField(
        max_length=300,
        verbose_name='Наименование'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='Категория'
    )
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Базовая цена'
    )
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='pcs',
        verbose_name='Единица измерения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['sku'])
        ]

    def __str__(self):
        return f'{self.sku} — {self.name}'