from rest_framework import serializers
from entities.models import *


class UserRoleAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoleAttribute
        fields = '__all__'


class AttributeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = '__all__'


class AttributeSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeSet
        fields = '__all__'
