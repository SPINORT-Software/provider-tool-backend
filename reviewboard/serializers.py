from rest_framework.serializers import ModelSerializer
from .models import *


class ClientReferralSerializer(ModelSerializer):
    class Meta:
        model = ClientReferral
        fields = '__all__'
