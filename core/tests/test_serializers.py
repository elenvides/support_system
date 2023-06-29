from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from core.serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    UserCreateRequestSerializer,
    UserCreateResponseSerializer,
    UserCreateSerializer,
    UserPublicSerializer,
)

User = get_user_model()


class UserCreateSerializerTestCase(TestCase):
    def test_valid_serializer(self):
        data = {"email": "test@example.com", "password": "testpassword"}
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email_serializer(self):
        data = {"email": "invalid-email", "password": "testpassword"}
        serializer = UserCreateSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_missing_fields_serializer(self):
        data = {"email": "test@example.com"}
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class UserPublicSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@example.com", role=2)

    def test_valid_serializer(self):
        serializer = UserPublicSerializer(self.user)
        expected_data = {
            "id": self.user.id,
            "email": "test@example.com",
            "first_name": None,
            "last_name": None,
            "role": 2,
        }
        self.assertEqual(serializer.data, expected_data)


class UserCreateRequestSerializerTest(TestCase):
    def test_valid_serializer(self):
        data = {"email": "test@example.com", "password": "password123", "role": 3}
        serializer = UserCreateRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer_missing_field(self):
        data = {"email": "test@example.com", "password": "password123"}
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
        data = {
            "user_id": 1,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "token": "123abc",
        }
        serializer = LoginResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.data, data)
