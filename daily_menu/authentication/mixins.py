from django.contrib.auth import get_user_model


User = get_user_model()


class ClientCredentialsMixin:
    def login_client_with_superuser(self):
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
