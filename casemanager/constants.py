from .serializers import ExistingEMCAssessmentSerializer, NewEMCAssessmentSerializer, ClientReAssessmentSerializer

CLIENT_ASSESSMENT_TYPE_SERIALIZER = {
    'EXISTING_EMC_NO_REASSESS': ExistingEMCAssessmentSerializer,
    'EXISTING_EMC_REASSESS': (ExistingEMCAssessmentSerializer, ClientReAssessmentSerializer),
    'NEW_EXTRA_MURAL_CLIENT': NewEMCAssessmentSerializer,
    'EXISTING_CASE_CLIENT_REASSESS': ClientReAssessmentSerializer
}

CLIENT_ASSESSMENT_TYPE_FIELD = {
    'EXISTING_EMC_NO_REASSESS': 'existing_assessment',
    'EXISTING_EMC_REASSESS': ('existing_assessment', 'reassessment'),
    'NEW_EXTRA_MURAL_CLIENT': 'newextramuralclient_assessment',
    'EXISTING_CASE_CLIENT_REASSESS': 'reassessment'
}

