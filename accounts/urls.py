from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)
from .views import register_json

urlpatterns = [
    path('register/', register_json, name='register_json'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token/obtain/', obtain_jwt_token),
    path('auth/token/refresh/', refresh_jwt_token),
    path('auth/token/verify/', verify_jwt_token),
]
