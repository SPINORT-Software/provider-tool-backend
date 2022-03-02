from rest_framework import serializers

from authentication.serializers import UserDetailSerializer
from casemanager.serializers import CaseManagerClientAssessmentBasicDataSerializer, \
    ClientInterventionBasicDataSerializer
from clinician.serializers import ClientAssessmentBasicDataSerializer, ClientInterventionSerializer

from .models import SharerCommunication, ActivityNotifications, ActivityNotificationsRead
from casemanager.models import CaseManagerClientAssessment, ClientIntervention
from clinician.models import ClinicianClientAssessment, ClinicianClientInterventions

CommunicationContentTypeClassSerializers = {
    CaseManagerClientAssessment: CaseManagerClientAssessmentBasicDataSerializer,
    ClinicianClientAssessment: ClientAssessmentBasicDataSerializer,
    ClientIntervention: ClientInterventionBasicDataSerializer,
    ClinicianClientInterventions: ClientInterventionSerializer
}


class SharerCommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharerCommunication
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['communication_by'] = UserDetailSerializer(instance.communication_by.user).data
        return response


class ReferralsAndFollowUpsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharerCommunication
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['communication_by'] = UserDetailSerializer(instance.communication_by.user).data
        response['communication_type'] = instance.get_communication_type_display()
        response['communication_type_id'] = instance.communication_type
        response['mode_of_communication'] = instance.get_mode_of_communication_display()

        # Content Type and Communication Object Serialized
        content_type_model = instance.content_type.model_class()
        content_type_model_serializer = CommunicationContentTypeClassSerializers.get(content_type_model)
        response['communication_object'] = content_type_model_serializer(instance.communication_object).data
        response['content_type_code'] = instance.content_type.model_class().__name__
        response['content_type'] = instance.content_type.model_class()._meta.verbose_name.title()

        return response


class SharerCommunicationRequestDataSerializer(serializers.Serializer):
    from_user = serializers.UUIDField()
    to_user = serializers.UUIDField()
    type = serializers.IntegerField(min_value=0, max_value=4)
    mode = serializers.IntegerField(min_value=0, max_value=7, required=False, default=0)
    instance_object = serializers.UUIDField()
    instance_type = serializers.IntegerField(min_value=1,
                                             max_value=4)  # Client assessment, Client intervention for CM and Clinician
    discussion_details = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        optional_fields = ['discussion_details', 'mode']


class ActivityNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityNotifications
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['timesince'] = instance.timesince
        return response


class ActivityNotificationsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityNotificationsRead
        fields = '__all__'
