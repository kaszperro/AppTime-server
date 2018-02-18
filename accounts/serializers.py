from rest_framework import serializers
from .models import User
from drf_queryfields import QueryFieldsMixin


class UserSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'name', 'email', 'phone_number', 'surname')
