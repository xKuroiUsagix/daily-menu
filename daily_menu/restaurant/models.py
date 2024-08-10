from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=128, unique=True)


class DailyMenu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=128, unique=True)
    date = models.DateField()
    description = models.TextField()
    
    class Meta:
        unique_together = ['restaurant', 'date']
    

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()


class MenuDish(models.Model):
    menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['menu', 'dish']
