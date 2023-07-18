from django.urls import path
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import LoginResponseSerializer

urlpatterns = [
    path(
        "token/",
        swagger_auto_schema(
            method="post",
            responses={
                201: openapi.Response("response description", LoginResponseSerializer)
            },
        )(TokenObtainPairView.as_view()),
    ),
]
