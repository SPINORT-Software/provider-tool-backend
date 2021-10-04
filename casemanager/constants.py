from .serializers import ExistingEMCAssessmentSerializer, NewEMCAssessmentSerializer, ClientReAssessmentSerializer

CLIENT_ASSESSMENT_TYPE_SERIALIZER = {
    'NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS': ExistingEMCAssessmentSerializer,
    'NEW_CASE_CLIENT_EXISTING_EMC_REASSESS': (ExistingEMCAssessmentSerializer, ClientReAssessmentSerializer),
    'NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT': NewEMCAssessmentSerializer,
    'EXISTING_CASE_CLIENT_REASSESS': ClientReAssessmentSerializer
}

CLIENT_ASSESSMENT_FIELD_SERIALIZER = {
    'existing_assessment': ExistingEMCAssessmentSerializer,
    'reassessment': ClientReAssessmentSerializer
}

CLIENT_ASSESSMENT_TYPE_FIELD = {
    'NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS': 'existing_assessment',
    'NEW_CASE_CLIENT_EXISTING_EMC_REASSESS': ('existing_assessment', 'reassessment'),
    'NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT': 'newextramuralclient_assessment',
    'EXISTING_CASE_CLIENT_REASSESS': 'reassessment'
}
