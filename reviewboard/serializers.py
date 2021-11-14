from rest_framework.serializers import ModelSerializer
from .models import *


class ReviewBoardUserSerializer(ModelSerializer):
    class Meta:
        model = ReviewBoardUser
        fields = '__all__'


class ClientReferralSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['review_board_user'] = ReviewBoardUserSerializer(instance.review_board_user).data
        return response

    class Meta:
        model = ClientReferral
        fields = '__all__'
