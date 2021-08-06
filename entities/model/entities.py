from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import EntityType
from django.db.utils import IntegrityError, DatabaseError, Error
from django.core import serializers


class EntityTypeModel:
    """
    All CRUD operations of EntityType model.
    """

    def create_entity_type(self, entity_type_data):
        """
        Create an EntityType record.
        :param entity_type_data:
        :return: HttpResponse
        """
        try:
            entity_type_created = EntityType()
            entity_type_created.entity_type_label = entity_type_data.get("label")
            entity_type_created.entity_type_code = entity_type_data.get("code")
            entity_type_created.save()
            return HttpResponse(result=True, message="Entity Type creation success.", status=status.HTTP_200_OK,
                                id="Entity Type ID",
                                id_value=entity_type_created.entity_type_id)
        except Error as e:
            return HttpResponse(result=False, message="Could not create entity type." + str(e),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_entity_type(self):
        """
        List of all EntityType records.
        :return: HttpResponse
        """
        try:
            response_json = EntityType.objects.values()
            return HttpResponse(result=True, message="Entity list generated successfully.", status=status.HTTP_200_OK,
                                value=response_json)
        except Error as e:
            return HttpResponse(result=False, message="Could not list entity type values.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
