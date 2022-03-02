from core.serializers.models import ExistingEMCAssessmentSerializer, NewEMCAssessmentSerializer, ClientReAssessmentSerializer
from casemanager.models import CaseManagerClientAssessment, ClientIntervention
from clinician.models import ClinicianClientAssessment, ClinicianClientInterventions

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

USER_TYPE_CLINICIAN = 'USER_TYPE_CLINICIAN'
USER_TYPE_CASE_MANAGER = 'USER_TYPE_CASE_MANAGER'

NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS'
NEW_CASE_CLIENT_EXISTING_EMC_REASSESS = 'NEW_CASE_CLIENT_EXISTING_EMC_REASSESS'
NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT = 'NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT'
EXISTING_CASE_CLIENT_REASSESS = 'EXISTING_CASE_CLIENT_REASSESS'


"""
Internal Referral for Client Assessments, Client Interventions 
"""
COMMUNICATION_OBJECT_INSTANCE_TYPES = {
    1: ClinicianClientAssessment,
    2: CaseManagerClientAssessment,
    3: ClientIntervention,
    4: ClinicianClientInterventions
}

WS_CONSUMER_GROUPS = {
    "MESSAGING": "MESSAGING_CHANNEL_GROUP",
    "NOTIFICATIONS": "ACTIVITY_NOTIFICATIONS_CHANNEL_GROUP"
}