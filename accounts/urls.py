from django.urls import path, include
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token
)
from .views import (
    register_html,
    example_view,
    register
)

urlpatterns = [
    path('register-html/', register_html, name='register_html'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/token/obtain/', obtain_jwt_token, name='obtain-token'),
    path('auth/token/refresh/', refresh_jwt_token, name='refresh-token'),
    path('auth/token/verify/', verify_jwt_token, name='verify-token'),
    path('register/', register, name='register'),
    path('test/', example_view)
]
