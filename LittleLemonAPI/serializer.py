from rest_framework import serializers
from .models import MenuItem,Category
from django.contrib.auth.models import User,Group



class CategorySerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','category','featured']

class GroupSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Group
        fields = ('name',)

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True,many=True)
    class Meta:
        model = User
        fields = ('id','username', 'groups',)
