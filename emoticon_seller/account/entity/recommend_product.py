from django.db import models

from account.entity.account import Account


class RecommendProduct(models.Model):
    productIdList = models.CharField(max_length=128)
    account = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"RecommendProduct -> idList: {self.idList}"

    class Meta:
        db_table = 'recommend_product'
        app_label = 'account'