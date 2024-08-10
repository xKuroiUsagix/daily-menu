from datetime import date

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import Restaurant, DailyMenu


User = get_user_model()


class RestaurantTests(APITestCase):
    def setUp(self) -> None:
        username = 'superuser'
        password = 'test_pass'
        
        self.user = User(username=username)
        self.user.set_password(password)
        self.user.is_superuser = True
        self.user.save()

        data = {
            'username': username,
            'password': password
        }
    
        response = self.client.post('/api/auth/token/', data, format='json')
        token = response.data.get('access')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.path = '/api/restaurants/'
        self.name = 'Restaurant Name'
    
    def test_create_restaurant(self):
        data = {
            'name': self.name
        }
        response = self.client.post(self.path, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, self.name)


class DailyMenuTests(APITestCase):
    def setUp(self) -> None:
        username = 'superuser'
        password = 'test_pass'
        
        self.user = User(username=username)
        self.user.set_password(password)
        self.user.is_superuser = True
        self.user.save()

        data = {
            'username': username,
            'password': password
        }
    
        response = self.client.post('/api/auth/token/', data, format='json')
        token = response.data.get('access')
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.restaurant = Restaurant.objects.create(name='Test Name')
        self.menu_name = 'Test Menu'
        self.description = 'Test Description'
        self.path = '/api/menus/'
        self.valid_data = {
            'restaurant': self.restaurant.id,
            'name': self.menu_name,
            'description': self.description,
            'date': date(2024, 8, 10)
        }
        
        self.duplicated_restaurant = Restaurant.objects.create(name='Duplicated Restaurant')
        self.duplicated_menu_data = {
            'restaurant': self.duplicated_restaurant,
            'name': 'duplciated menu',
            'description': self.description,
            'date': date(2024, 8, 10)
        }
        
        DailyMenu.objects.create(**self.duplicated_menu_data)
    
    def test_create_menu(self):
        response = self.client.post(self.path, self.valid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DailyMenu.objects.count(), 2)
        self.assertTrue(DailyMenu.objects.filter(name=self.menu_name).exists())
    
    def test_create_2_menu_in_one_day(self):
        self.duplicated_menu_data['restaurant'] = self.duplicated_restaurant.id
        response = self.client.post(self.path, self.duplicated_menu_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
