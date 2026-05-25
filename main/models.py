from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Manufacturer(models.Model):
    name = models.CharField(max_length = 100)
    country = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 200)
    description = models.TextField()
    photo = models.ImageField(upload_to = 'products/', blank = True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2, 
    validators = [MinValueValidator(0)])
    stock = models.IntegerField(validators = [MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_create = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"Корзина пользователя {self.user.username}"
    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.product.price * item.quantity
        return total

class ElemCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product.name}({self.quantity})"
        def item_price(self):
            return self.product.price * self.quantity