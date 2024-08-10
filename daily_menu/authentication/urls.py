from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)

from .views import (
    CreateUserAPIView,
    UserAPIView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/create/', CreateUserAPIView.as_view(), name='create_user'),
    path('user/', UserAPIView.as_view(), name='retrieve_user')
]
