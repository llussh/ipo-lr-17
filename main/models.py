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
      return sum(item.product.price * item.quantity for item in self.elemcart_set.all())


class ElemCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.product.name}({self.quantity})"
        def item_price(self):
            return self.product.price * self.quantity
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменён'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # цена на момент покупки
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"