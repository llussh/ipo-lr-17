from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
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
    phone = models.CharField(max_length=20, blank=True, null=True)  
    address = models.TextField(blank=True, null=True)  
    comment = models.TextField(blank=True, null=True)  
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # цена на момент покупки
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
class Profile(models.Model):
    ROLE_CHOICES = [
        ('CUSTOMER', 'Клиент'),
        ('MANAGER', 'Менеджер'),
        ('ADMIN', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER', verbose_name='Роль')
    
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес доставки')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return f"Профиль: {self.user.username} ({self.get_role_display()})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=[('CUSTOMER', 'Клиент'), ('MANAGER', 'Менеджер'), ('ADMIN', 'Администратор')], default='CUSTOMER', verbose_name='Роль')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='ФИО')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес доставки')
    district = models.CharField(max_length=100, blank=True, null=True, verbose_name='Микрорайон Минска')
    postal_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='Почтовый индекс')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль: {self.user.username} ({self.get_role_display()})"
