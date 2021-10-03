from .serializers import ExistingEMCAssessmentSerializer, NewEMCAssessmentSerializer, ClientReAssessmentSerializer

CLIENT_ASSESSMENT_TYPE_SERIALIZER = {
    'EXISTING_NO_REASSESS': ExistingEMCAssessmentSerializer,
    'EXISTING_REASSESS': (ExistingEMCAssessmentSerializer, ClientReAssessmentSerializer),
    'NEW_EXTRA_MURAL': NewEMCAssessmentSerializer,
    'EXISTING_CASE_CLIENT_REASSESS': ClientReAssessmentSerializer
}

CLIENT_ASSESSMENT_TYPE_FIELD = {
    'EXISTING_NO_REASSESS': 'existing_assessment',
    'EXISTING_REASSESS': ('existing_assessment', 'reassessment'),
    'NEW_EXTRA_MURAL': 'newextramuralclient_assessment',
    'EXISTING_CASE_CLIENT_REASSESS': 'reassessment'
}

