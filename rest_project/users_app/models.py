from django.db import models
from rest_app.models import Product
from django.contrib.auth.models import User

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