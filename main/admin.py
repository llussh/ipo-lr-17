from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, ElemCart
from .models import Profile

admin.site.register(Manufacturer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(ElemCart)
admin.site.register(Profile)