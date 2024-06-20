from django.db import models


class RoleType(models.TextChoices):
    ADMIN = 'ADMIN'
    CUSTOMER = 'CUSTOMER'
    SELLER = 'SELLER'
    BLACKLIST = 'BLACKLIST'