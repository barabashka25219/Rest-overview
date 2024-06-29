from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name