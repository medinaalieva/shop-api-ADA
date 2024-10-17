from django.db import models
from django.contrib.auth import get_user_model

from apps.product.models import Product

User = get_user_model()


class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'Too Bad'),
        (2, 'Bad'),
        (3, 'Ok'),
        (4, 'Good'),
        (5, 'Perfect')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'product']
        # 1  3
        # 1  3 error