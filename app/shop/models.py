from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256)

class Product(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

# User ??

class Basket(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    # poduct_quantity ?? czy pole tu czy w product?
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # user

class Loyalty_program(models.Model):
    #user
    points = models.PositiveIntegerField()


class Comment(models.Model):
    content = models.TextField()
    date_add = models.DateField(auto_now=True)
    #user
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
