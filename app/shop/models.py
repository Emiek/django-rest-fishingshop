from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""

        if not email:
            raise ValueError('User must have an email address')

        user: 'User' = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    name = models.CharField(max_length=256)


class Product(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=10000)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey


class Basket(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    poduct_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Loyalty_program(models.Model):
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    points = models.PositiveIntegerField()


class Comment(models.Model):
    content = models.TextField()
    date_add = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
