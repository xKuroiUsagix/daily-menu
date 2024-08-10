from datetime import date

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework import status
from rest_framework.decorators import action

from authentication.permissions import IsAdminOrReadOnly
from .serializers import (
    RestaurantSerializer,
    DishSerializer,
    DailyMenuSerializer,
    MenuDishSerializer
)
from .models import (
    Restaurant, 
    Dish, 
    DailyMenu,
    MenuDish
)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def dishes(self, request, pk):
        dishes = Dish.objects.filter(restaurant__id=pk)
        serializer = DishSerializer(instance=dishes, many=True)
        return Response(serializer.data)


class DishViewSet(ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminOrReadOnly]


class DailyMenuViewSet(ModelViewSet):
    queryset = DailyMenu.objects.all()
    serializer_class = DailyMenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['post'])
    def add_dish(self, request, pk):
        data = request.data.copy()
        data['menu'] = pk
    
        serializer = MenuDishSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def dishes(self, request, pk):
        menu_dishes = MenuDish.objects.filter(menu__id=pk).only('dish')
        dishes = [md.dish for md in menu_dishes]
        serializer = DishSerializer(instance=dishes, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        menus = DailyMenu.objects.filter(date=date.today())
        serializer = DailyMenuSerializer(instance=menus, many=True)
        return Response(serializer.data)
