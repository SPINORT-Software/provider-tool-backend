from rest_framework.serializers import ModelSerializer
from .models import *


class ReviewBoardUserSerializer(ModelSerializer):
    class Meta:
        model = ReviewBoardUser
        fields = '__all__'


class ClientReferralSerializer(ModelSerializer):
    review_board_user = ReviewBoardUserSerializer()
    class Meta:
        model = ClientReferral
        fields = '__all__'
