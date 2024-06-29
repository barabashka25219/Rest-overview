from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
        default_related_name = 'basket_product'

    def __str__(self):
        return self.product.name


class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    grade = models.SmallIntegerField(default=5)
    text = models.TextField(max_length=2048, null=True, blank=True)

    class Meta:
        ordering = ['user']
        default_related_name = 'feedbacks'

    def __str__(self):
        return self.product.name