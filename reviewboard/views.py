from .serializers import *
import copy
from documents.serializers import ReviewBoardReferralFormsDocumentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
import json
from rest_framework import generics


class ClientReferralList(generics.ListCreateAPIView):
    """
    List all client referral.
    """
    queryset = ClientReferral.objects.all()
    serializer_class = ClientReferralSerializer


class ClientReferralCreate(APIView):
    """
    Create a new client referral.
    """

    def post(self, request):
        try:
            if 'data' not in request.data:
                return Response({
                    'result': False,
                    'message': 'Invalid client referral request data'
                }, status=HTTP_400_BAD_REQUEST)

            referral_data = copy.deepcopy(request.data['data'])

            if "organizations_upon_referral" in referral_data:
                clinical_type_json = json.dumps(referral_data["organizations_upon_referral"])
                referral_data["organizations_upon_referral"] = clinical_type_json

            if "members_present_case_discussion" in referral_data:
                clinical_type_json = json.dumps(referral_data["members_present_case_discussion"])
                referral_data["members_present_case_discussion"] = clinical_type_json

            serializer = ClientReferralSerializer(data=referral_data)
            if serializer.is_valid():
                client_referral = serializer.save()
                if client_referral:
                    forms_request_data = request.data["referral_forms"]
                    forms_create_result = self.create_referral_forms(client_referral, forms_request_data)

                    if forms_create_result:
                        return Response({
                            'result': True,
                            'message': 'Client Referral record created.'
                        }, status=HTTP_201_CREATED)
                    else:
                        return Response({
                            'result': True,
                            'message': 'Failed to create Client Referral record.'
                        }, status=HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        'result': False,
                        'message': 'Failed to create Client Referral record.'
                    }, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(serializer.errors)
                return Response({
                    'result': False,
                    'message': 'Invalid referral request data'
                }, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
            return Response({
                'result': False,
                'message': 'Failed to process your request. '
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def create_referral_forms(self, client_referral, forms_request_data):
        referralFormsCreate = True
        if isinstance(forms_request_data, dict):
            for form in forms_request_data:
                if isinstance(forms_request_data[form], list):
                    for form_document in forms_request_data[form]:
                        serializer_data = {
                            "document": form_document,
                            "client_referral": client_referral.referral_id
                        }
                        form_document_serializer = ReviewBoardReferralFormsDocumentsSerializer(data=serializer_data)
                        if form_document_serializer.is_valid():
                            form_document_serializer.save()
                        else:
                            referralFormsCreate = False
        else:
            return False

        return referralFormsCreate
