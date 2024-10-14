from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.category.models import Category

User = get_user_model()


class Product(models.Model):
    STOCK_CHOICES = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии')
    )
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product-image/')
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='products')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    quantity = models.IntegerField(validators=[
        MinValueValidator(0)
    ])
    stock = models.CharField(max_length=20, choices=STOCK_CHOICES)
    discount = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ])

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.stock = 'in_stock'
        else:
            self.stock = 'out_of_stock'
        return super().save(*args, **kwargs)
