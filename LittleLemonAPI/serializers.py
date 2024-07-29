from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Cart, MenuItem, Category, Order, OrderItem
from django.contrib.auth.models import User, Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category', 'featured', 'category_id']
        

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'groups']

class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id']
        extra_kwargs = {
            'user': {'read_only': True},
            'unit_price': {'read_only': True},
            'price': {'read_only': True},
            'quantity': {'min_value': 1},
        }
    

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'order': {'read_only': True},
            'unit_price': {'read_only': True},
            'price': {'read_only': True},
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'items']
        extra_kwargs = {
            'user': {'read_only': True},
            'total': {'read_only': True},
            'date': {'read_only': True},
        }
