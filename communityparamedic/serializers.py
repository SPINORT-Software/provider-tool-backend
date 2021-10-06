from rest_framework.serializers import ModelSerializer
from .models import DailyWorkLoad


class DailyWorkloadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'
