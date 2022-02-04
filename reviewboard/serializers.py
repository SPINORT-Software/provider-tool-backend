from rest_framework.serializers import ModelSerializer
from .models import *
from documents.models import ReviewBoardReferralFormsDocuments
from documents.serializers import ReviewBoardReferralFormsDocumentsSerializer
from authentication.models import ApplicationUser


class ReviewBoardUserSerializer(ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = '__all__'


class ClientReferralSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['review_board_user'] = ReviewBoardUserSerializer(instance.review_board_user).data

        referral_forms = ReviewBoardReferralFormsDocuments.objects.filter(client_referral=instance)
        response['referral_forms'] = ReviewBoardReferralFormsDocumentsSerializer(referral_forms, many=True).data
        return response

    class Meta:
        model = ClientReferral
        fields = '__all__'
        extra_kwargs = {"review_board_user": {"error_messages": {
            "required": "Review board user necessary to create client referral record.",
            "does_not_exist": "Provided Review board user does not exist."
        }}}
