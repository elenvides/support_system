import json

from django.contrib.auth import get_user_model
from django.test import TestCase

# isort: off
from core.serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
)

# isort: on

User = get_user_model()


class UserCreateRequestSerializerTest(TestCase):
    def test_valid_serializer(self):
        data = {"email": "test@example.com", "password": "password123", "role": 3}
        serializer = UserCreateRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_missing_field(self):
        data = {"email": "test@example.com"}
        serializer = UserCreateRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class UserCreateResponseSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", role=3)

    def test_serializer(self):
        serializer = UserCreateResponseSerializer(self.user)
        expected_data = {
            "id": self.user.id,
            "email": "test@example.com",
            "first_name": None,
            "last_name": None,
            "role": 3,
        }
        self.assertDictEqual(serializer.data, expected_data)


class LoginRequestSerializerTest(TestCase):
    def test_valid_serializer(self):
        data = {"email": "test@example.com", "password": "password123"}
        serializer = LoginRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_missing_field(self):
        data = {"email": "test@example.com"}
        serializer = LoginRequestSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class LoginResponseSerializerTest(TestCase):
    def test_serializer(self):
        user_obj = User.objects.create(
            email="test@example.com", first_name="John", last_name="Doe", role=1
        )
        input_data = {"user": user_obj, "token": "123abc"}

        serializer = LoginResponseSerializer(input_data)

        expected_data = {
            "user": {
                "id": user_obj.id,
                "email": "test@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": 1,
            },
            "token": "123abc",
        }

        self.assertEqual(
            json.dumps(serializer.data, sort_keys=True),
            json.dumps(expected_data, sort_keys=True),
        )
