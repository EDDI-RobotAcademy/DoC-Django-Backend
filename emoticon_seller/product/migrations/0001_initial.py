# Generated by Django 5.0.6 on 2024-06-26 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("productId", models.AutoField(primary_key=True, serialize=False)),
                ("productName", models.CharField(max_length=128)),
                ("productPrice", models.IntegerField()),
                ("productCategory", models.CharField(max_length=10)),
                ("writer", models.CharField(max_length=32)),
                ("content", models.TextField()),
                ("productImage", models.CharField(max_length=100)),
                ("regDate", models.DateTimeField(auto_now_add=True)),
                ("updDate", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "product",
            },
        ),
    ]
