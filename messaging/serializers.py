from rest_framework import serializers
from .models import Message
from authentication.models import User
from authentication.serializers import UserSearchSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['sender'] = UserSearchSerializer(instance.sender).data
        response['recipient'] = UserSearchSerializer(instance.recipient).data
        return response


class ShareSerializer(serializers.Serializer):
    share_type = serializers.CharField(max_length=56)
    share = serializers.UUIDField()
    sharer = User
    share_to = User
