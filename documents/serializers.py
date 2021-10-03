from rest_framework.serializers import ModelSerializer
from .models import *


class AssessmentFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = AssessmentFormsDocuments
        fields = '__all__'
