from rest_framework import serializers
from entities.models import *


class UserRoleAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleAttribute
        fields = '__all__'
