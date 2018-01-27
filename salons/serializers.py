from rest_framework import serializers
from salons.models import Salon

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = ('pk', 'name')
