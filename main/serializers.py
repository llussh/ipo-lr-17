from rest_framework import serializers
from .models import Product, Category, Manufacturer, Cart, ElemCart, Profile,Order
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
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'role', 'full_name', 'phone', 'address']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', required=False) 

    class Meta:
        model = Profile
        fields = ['username', 'email', 'role', 'full_name', 'phone', 'address', 'district', 'postal_code']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'email' in user_data:
            instance.user.email = user_data['email']
            instance.user.save()
        return super().update(instance, validated_data)
