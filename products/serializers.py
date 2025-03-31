# products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'stock_status', 'sku', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        # Additional validation can be added here
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return data