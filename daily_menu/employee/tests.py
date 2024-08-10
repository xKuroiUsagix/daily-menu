from datetime import date

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from restaurant.models import Restaurant, DailyMenu
from .models import EmployeeVote, Employee


User = get_user_model()


@freeze_time('2024-08-10')
class EmployeeVoteTests(APITestCase):
    def setUp(self) -> None:
        users = self._create_users()
        self.employees = self._create_employees(users)
        restaurants = self._create_restaurants()
        self.menus = self._create_menus(restaurants)

        self._login_client()
        self.votes_path = '/api/votes/'
        self.todays_choice_path = '/api/votes/todays_choice/'
    
    def test_create_employee_vote(self):
        data = {
            'menu': self.menus[0].id,
            'employee': self.employees[0].id
        }
        response = self.client.post(self.votes_path, data, form='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmployeeVote.objects.count(), 1)
    
    def test_todays_choice(self):
        self._vote_for_menu(self.menus[0])
        response = self.client.get(self.todays_choice_path)
        
        expected_votes_count = len(self.employees)
        exptected_menu_name = self.menus[0].name
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('votes'), expected_votes_count)
        self.assertEqual(response.data.get('name'), exptected_menu_name)
        
    def _login_client(self):
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
        
    
    def _create_users(self):
        return User.objects.bulk_create([
            User(username=f'test_user_{i}', password=f'test_pass_{i}')
            for i in range(3)
        ])
    
    def _create_employees(self, users):
        return Employee.objects.bulk_create([
            Employee(
                user=user,
                name=f'name_{user.id}',
                surname=f'surname_{user.id}'
            )
            for user in users
        ])
    
    def _create_restaurants(self):
        return Restaurant.objects.bulk_create([
            Restaurant(name=f'test_restaurant_{i}')
            for i in range(2)
        ])
    
    def _create_menus(self, restaurants):
        return DailyMenu.objects.bulk_create([
            DailyMenu(
                restaurant=restaurant,
                name=f'test_name_{restaurant.id}',
                date=date(2024, 8, 10),
                description='test description'
            )
            for restaurant in restaurants
        ])
    
    def _vote_for_menu(self, menu):
        EmployeeVote.objects.bulk_create([
            EmployeeVote(
                employee=employee,
                menu=menu
            )
            for employee in self.employees
        ])
