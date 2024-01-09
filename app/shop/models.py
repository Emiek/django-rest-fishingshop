from django.db import models
from user.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)


class Product(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    amount_rating = models.PositiveIntegerField(null=True, default=0)
    total_rating = models.FloatField(null=True, default=0)
    rating = models.FloatField(null=True, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=2000)
    sold_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)
    img_url = models.URLField(null=True, default=None)
    points = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

    def stock_decrease(self, quantity):
        if self.stock >= quantity:
            self.stock = self.stock - quantity
            self.save()
        else:
            raise Exception('not enough products in store')

    def add_sold_count(self):
        self.sold_count = self.sold_count + 1
        self.save()


class FavouriteProduct(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    date_add = models.DateField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_loyalty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()
    is_paid = models.BooleanField(default=False)

    def sum_price_points(self):
        if self.pk:
            self.total_price = sum(item.price for item in self.orderitem_set.all())
            self.total_loyalty = sum(item.loyalty_p for item in self.orderitem_set.all())

    def save(self, *args, **kwargs):
        if self.is_paid:
            for order_item in self.orderitem_set.all():
                order_item.product.stock_decrease(order_item.quantity)
                order_item.product.add_sold_count()
            self.user.points = self.user.points + self.total_loyalty
            self.user.save(update_fields=['points'])
        if not self.pk:  # Check if the instance is unsaved
            self.sum_price_points()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loyalty_p = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def loyalty_p_price_sum(self):
        if self.product:
            self.loyalty_p = self.product.points * self.quantity
            self.price = self.product.price * self.quantity

    def save(self, *args, **kwargs):
        self.loyalty_p_price_sum()
        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    rating = models.PositiveIntegerField()
    date_add = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)

    def rating_calculation(self):
        self.product.amount_rating = self.product.amount_rating + 1
        self.product.total_rating = self.rating + self.product.total_rating
        self.product.rating = self.product.total_rating / self.product.amount_rating

    def save(self, *args, **kwargs):
        self.rating_calculation()
        super().save(*args, **kwargs)
        self.product.save(update_fields=['amount_rating', 'rating', 'total_rating'])
