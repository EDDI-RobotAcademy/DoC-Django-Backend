from django.db import models

from product.entity.models import Product


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    reviewTitle = models.CharField(max_length=128, null=False)
    reviewWriter = models.CharField(max_length=32, null=False)
    reviewContent = models.TextField()
    reviewRating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0,null=False)
    reviewImage = models.CharField(max_length=100, null=True)
    reviewRegDate = models.DateTimeField(auto_now_add=True)
    reviewUpdDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reviewTitle

    class Meta:
        db_table = 'review'
