from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(max_length=250)


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


# region HW
class UserCreateRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    role = serializers.IntegerField()


class UserCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField(max_length=150)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    token = serializers.CharField()


# endregion HW
