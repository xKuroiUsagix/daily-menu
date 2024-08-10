from rest_framework.routers import DefaultRouter

from .views import (
    RestaurantViewSet, 
    DishViewSet, 
    DailyMenuViewSet,
)


router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('dishes', DishViewSet, basename='dish')
router.register('menus', DailyMenuViewSet, basename='menu')


urlpatterns = router.urls
