from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.constants import Role

User = get_user_model()


# class UserCreateSerializer(serializers.Serializer):
#     email = serializers.EmailField(max_length=150)
#     password = serializers.CharField(max_length=250)
#
#
# class UserPublicSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "email", "first_name", "last_name", "role"]


class UserCreateRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    role = serializers.IntegerField(default=Role.USER)


class UserCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = UserCreateResponseSerializer()
    token = serializers.CharField()
