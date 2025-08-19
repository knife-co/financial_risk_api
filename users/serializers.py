# users/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile data
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number']
    
    def validate(self, data):
        """
        Validate that passwords match
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        """
        Create user with hashed password
        """
        # Remove password_confirm from data
        validated_data.pop('password_confirm')
        
        # Create user with hashed password
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Inavlid usernameor password')

            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')

            data['user'] = user
            return data
        else:
            raise serializers.ValidationError('Must provide both username and password')

    def create(self, validated_data):
        # Override create to prevent actually creating a user during login
        # This method won't be called in login flow, but good practice to override
        raise NotImplementedError('Login serializer should not create users')

    def update(self, instance, validated_data):
        # Override update to prevent updating users during login
        raise NotImplementedError('Login serializer should not update users')

