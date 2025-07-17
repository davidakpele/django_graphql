from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'firstname', 'lastname', 'enabled', 'createdAt']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname',  'username', 'state']
        extra_kwargs = {
            'firstname': {'required': False},
            'lastname': {'required': False},
            'username': {'required': False},
        }


    def validate_username(self, value):
        """
        Validate the username.
        """
        if value and CustomUser.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Username is already taken.")
        return value


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'firstname', 'lastname', 'username','enabled','createdAt']
