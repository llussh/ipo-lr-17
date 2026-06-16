from rest_framework import serializers
from .models import Product, Category, Manufacturer, Cart, ElemCart
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ElemCartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ElemCart
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    items = ElemCartSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'