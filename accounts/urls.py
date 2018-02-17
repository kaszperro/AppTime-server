from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)
from .views import (
    register_html,
    example_view,
    register,
    validate_token,
    ObtainJSONWebToken
)

urlpatterns = [
    path('register-html/', register_html, name='register_html'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token/obtain/', ObtainJSONWebToken.as_view(), name='obtain-token'),
    path('auth/token/refresh/', refresh_jwt_token, name='refresh-token'),
    path('auth/token/verify/', validate_token, name='verify-token'),
    path('register/', register, name='register'),
    path('test/', example_view)
]
