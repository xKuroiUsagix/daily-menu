from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth import get_user_model


User = get_user_model()


class UserTests(APITestCase):
    def setUp(self) -> None:
        self.path = '/api/auth/user/create/'
        self.username = 'test_username'
        self.password = 'test_password'
        self.wrong_confirm_password = 'wrong_pass'
    
    def test_create_user_success(self):
        data = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.password
        }
        response = self.client.post(self.path, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, self.username)
    
    def test_wrong_confirm_pasword(self):
        data = {
            'username': self.username,
            'password': self.password,
            'confirm_password': self.wrong_confirm_password
        }
        response = self.client.post(self.path, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class TokenTests(APITestCase):
    def setUp(self) -> None:
        self.path = '/api/auth/token/'
        
        self.username = 'test_username'
        self.password = 'test_password'

        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        
        self.valid_user_data = {
            'username': self.username,
            'password': self.password
        }

    def test_obtain_token_pair(self):
        response = self.client.post(self.path, self.valid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('access'))
        self.assertIsNotNone(response.data.get('refresh'))
    
    def test_obtain_token_pair_wrong_credentials(self):
        data = {
            'username': 'unexisting_user',
            'password': 'wrong_password'
        }
        response = self.client.post(self.path, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
