from rest_framework import serializers
from .models import Inventory, Product, OrderLine, SelectedItem,Comment,Todo
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  

class OrderLineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderLine
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    reorder_point = serializers.IntegerField(source='product.orderline.reorder_point', read_only=True)


    class Meta:
        model = Inventory
        fields = '__all__'  

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            password = validated_data['password'],
        )
        return user
    
class SelectedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectedItem
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields= '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
    