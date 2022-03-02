from rest_framework.views import APIView
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import *
from .serializers import *
from clinician.models import ClinicianClientAssessment, ClinicianClientInterventions
from casemanager.models import CaseManagerClientAssessment, ClientIntervention

import core.constants as constants


class SharerViews:
    class ShareListCreateView(APIView):
        def _get_communication_object(self, object_id, object_type):
            try:
                instance_type_model = constants.COMMUNICATION_OBJECT_INSTANCE_TYPES.get(object_type)
                return instance_type_model.objects.get(pk=object_id)
            except (ValueError, ValidationError, ClinicianClientAssessment.DoesNotExist,
                    CaseManagerClientAssessment.DoesNotExist):
                return False

        def _get_application_user_objects(self, communication_from_id, communication_to_id):
            try:
                from_object = ApplicationUser.objects.get(pk=communication_from_id)
                to_object = ApplicationUser.objects.get(pk=communication_to_id)

                return {'from': from_object,
                        'to': to_object}
            except ApplicationUser.DoesNotExist:
                return False

        def post(self, request):
            request_data = SharerCommunicationRequestDataSerializer(data=request.data)

            try:
                if request_data.is_valid():
                    communication_object_id = request_data.validated_data.get('instance_object')
                    communication_instance_type = request_data.validated_data.get('instance_type')

                    communication_object = self._get_communication_object(communication_object_id,
                                                                          communication_instance_type)

                    user_objects = self._get_application_user_objects(
                        request_data.validated_data.get('from_user'),
                        request_data.validated_data.get('to_user'))

                    if communication_object and user_objects:
                        communication_data = {
                            'communication_object': communication_object,
                            'communication_by': user_objects.get('from'),
                            'communication_to': user_objects.get('to'),
                            'communication_type': request_data.validated_data.get('type'),
                            'mode_of_communication': request_data.validated_data.get('mode'),
                            'discussion_details': request_data.validated_data.get('discussion_details'),
                        }
                        SharerCommunication.objects.create(**communication_data)
                        return Response({
                            'result': True,
                            'data': 'Communication sent.'
                        })
                    else:
                        return Response({
                            'result': False,
                            'data': 'Invalid data provided.'
                        })
                else:
                    print(request_data.errors)
                    return Response({
                        'result': False,
                        'data': 'Invalid communication data provided.'
                    })
            except Exception as e:
                return Response({
                    'result': False,
                    'data': 'Failed to send the communication data.'
                })

        def get(self, request, application_user_id):
            try:
                data = SharerCommunication.objects.filter(communication_to=application_user_id)
                return Response({
                    'result': True,
                    'data': SharerCommunicationSerializer(data, many=True).data
                }, status=HTTP_200_OK)
            except ApplicationUser.DoesNotExist:
                return Response({
                    'result': False
                }, status=HTTP_400_BAD_REQUEST)

    class ReferralListView(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            currentuser_uuid = request.user.application_user.app_user_id
            data = SharerCommunication.referrals.filter(communication_to=currentuser_uuid)

            return Response({
                'result': True,
                'data': ReferralsAndFollowUpsListSerializer(data, many=True).data
            })

    class ReferralListViewFilterByType(APIView):
        permission_classes = [IsAuthenticated]

        def __init__(self):
            self.referral_types = {
                "external": CommunicationTypeChoices.EXTERNAL_REFERRAL,
                "internal": CommunicationTypeChoices.INTERNAL_REFERRAL
            }

        def get(self, request, type):
            if type not in ["internal", "external"]:
                return Response({
                    'result': False
                })

            currentuser_uuid = request.user.application_user.app_user_id
            data = SharerCommunication.referrals.filter(communication_to=currentuser_uuid).filter(
                communication_type=self.referral_types.get(type))

            return Response({
                'result': True,
                'data': ReferralsAndFollowUpsListSerializer(data, many=True).data
            })

    class FollowUpListView(APIView):
        permission_classes = [IsAuthenticated]

        def get(self, request):
            currentuser_uuid = request.user.application_user.app_user_id
            data = SharerCommunication.followups.filter(communication_to=currentuser_uuid)

            return Response({
                'result': True,
                'data': ReferralsAndFollowUpsListSerializer(data, many=True).data
            })

    class FollowUpListViewFilterByType(APIView):
        permission_classes = [IsAuthenticated]

        def __init__(self):
            self.follow_up_types = {
                "external": CommunicationTypeChoices.EXTERNAL_FOLLOWUP,
                "internal": CommunicationTypeChoices.INTERNAL_FOLLOWUP
            }

        def get(self, request, type):
            if type not in ["internal", "external"]:
                return Response({
                    'result': False
                })

            currentuser_uuid = request.user.application_user.app_user_id
            data = SharerCommunication.followups.filter(communication_to=currentuser_uuid).filter(
                communication_type=self.follow_up_types.get(type))

            return Response({
                'result': True,
                'data': ReferralsAndFollowUpsListSerializer(data, many=True).data
            })

    class NotificationsListView(APIView):
        pass

    class NotificationsListAllView(ListAPIView):
        serializer_class = ActivityNotificationsSerializer
        queryset = ActivityNotifications.objects.all()

    class NotificationsRead(APIView):
        def post(self, request, pk):
            try:
                notification_read_user = request.user.application_user
                notification = ActivityNotifications.objects.get(pk=pk)
                notification_read = ActivityNotificationsRead.objects.create(
                    notification_id=notification,
                    application_user=notification_read_user
                )
                return Response({
                    "result": True,
                    "data": ActivityNotificationsReadSerializer(notification_read).data
                })

            except ActivityNotifications.DoesNotExist:
                return Response({
                    "result": False
                }, status=HTTP_400_BAD_REQUEST)

            except IntegrityError:
                return Response({
                    "result": False,
                    "message": "Invalid request - Notification already read by the user"
                }, status=HTTP_400_BAD_REQUEST)
