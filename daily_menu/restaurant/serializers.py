from rest_framework import serializers

from .models import Restaurant, DailyMenu, Dish, MenuDish


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name']
        read_only_fields = ['id']


class DailyMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMenu
        fields = ['id', 'restaurant', 'name', 'description', 'date']
        read_only_fields = ['id']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'restaurant', 'name', 'description']
        read_only_fields = ['id']


class MenuDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDish
        fields = ['menu', 'dish']
    
    def validate(self, data):
        validated_data = super().validate(data)

        menu = validated_data.get('menu')
        dish = validated_data.get('dish')
        
        if menu.restaurant != dish.restaurant:
            raise serializers.ValidationError('Menu and Dish must be from the same restaurant')
        
        return validated_data
