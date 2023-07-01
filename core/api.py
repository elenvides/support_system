from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from core.serializers import UserRegistrationSerializer

User = get_user_model()


class UserRegistrationAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        return super().post(request)
