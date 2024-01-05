from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)


class Product(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    amount_rating = models.PositiveIntegerField(null=True,default=None)
    total_rating = models.PositiveIntegerField(null=True,default=None)
    rating = models.PositiveIntegerField(null=True,default=None)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)
    img_url = models.URLField(null=True,default=None)
    points = models.PositiveIntegerField()

    def stock_decrease(self, quantity):
        if self.stock >= quantity:
            self.stock = self.stock - quantity
            self.save()
        else:
            raise Exception('not enough products in store')


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_loyalty = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_paid:
            for order_item in self.orderitem_set.all():
                order_item.product.stock_decrease(order_item.quantity)

    def sum_price_points(self):
        self.total_price = sum(item.price for item in self.orderitem_set.all())
        self.total_loyalty = sum(item.loyalty_p for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    loyalty_p = models.DecimalField(max_digits=10, decimal_places=2)

    def loyalty_p_sum(self):
        self.loyalty_p = self.product.points * self.quantity

    def save(self, *args, **kwargs):
        self.loyalty_p_sum()
        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_add = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
