from django.db import models
from django.contrib.auth import get_user_model

from restaurant.models import DailyMenu


User = get_user_model()


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)


class EmployeeVote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(DailyMenu, on_delete=models.CASCADE)
    voted_at = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'menu']
