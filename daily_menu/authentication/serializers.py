from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.core import exceptions

from rest_framework import serializers

from .constants import (
    PASSWORD_MAX_LENGTH, 
    PASSWORD_MIN_LENGTH, 
    USERNAME_MAX_LENGTH, 
    USERNAME_MIN_LENGTH,
)


User = get_user_model()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)


class RegisterUserSerializer(serializers.Serializer):
    username = serializers.CharField(
                    min_length=USERNAME_MIN_LENGTH, 
                    max_length=USERNAME_MAX_LENGTH
                )
    password = serializers.CharField(
                    min_length=PASSWORD_MIN_LENGTH, 
                    max_length=PASSWORD_MAX_LENGTH, 
                    write_only=True,
                    style={'input_type': 'password'}
                )
    confirm_password = serializers.CharField(
                    min_length=PASSWORD_MIN_LENGTH, 
                    max_length=PASSWORD_MAX_LENGTH,  
                    write_only=True,
                    style={'input_type': 'password'}
                )
    
    def validate(self, data):
        errors = {}
        validated_data = super().validate(data)
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')
        
        try:
           validate_password(password)
        except exceptions.ValidationError as e:
            errors['password'] = e.message

        if password != confirm_password:
            errors['confirm_password'] = 'password and confirm_password do not match'

        if errors:
            raise serializers.ValidationError(errors)
        
        return validated_data

    def save(self, **kwargs):
        return self.create(self.validated_data)
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
    
        user = User(username=username)
        user.set_password(password)
        user.save()
    
        return user
