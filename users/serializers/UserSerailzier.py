from rest_framework import serializers
from entities.models import UserEntity, Roles


class UserSerializer(serializers.ListSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
