from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import EntityType
from django.db.utils import IntegrityError, DatabaseError, Error
import uuid
from django.core.exceptions import ValidationError


class EntityTypeModel:
    """
    EntityType Model:
        All CRUD operations of EntityType model.
    """

    def create_entity_type(self, entity_type_data):
        """
        Create an EntityType record.
        :param entity_type_data:
        :return: HttpResponse
        """
        try:
            if all(key in entity_type_data for key in ("label", "code")):
                entity_type_created = EntityType()
                entity_type_created.entity_type_label = entity_type_data.get("label")
                entity_type_created.entity_type_code = entity_type_data.get("code")
                entity_type_created.save()
                return HttpResponse(result=True, message="Entity Type creation success.", status=status.HTTP_200_OK,
                                    id="Entity Type ID",
                                    id_value=entity_type_created.entity_type_id)
            else:
                return HttpResponse(result=False, message="Missing required request body fields.",
                                    status=status.HTTP_400_BAD_REQUEST)
        except Error as e:
            return HttpResponse(result=False, message=f"Could not create entity type. [{e.args[1]}]",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_entity_type(self):
        """
        List of all EntityType records.
        :return: HttpResponse
        """
        try:
            response_json = EntityType.objects.values()
            if len(response_json) > 0:
                return HttpResponse(result=True, message="Entity type list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)
            else:
                return HttpResponse(result=True, message="No Entity type found.",
                                    status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Could not list entity type values.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_entity_type_detail(self, entity_type_id):
        """
        Get EntityType detail.
        :param entity_type_id:
        :return:
        """
        try:
            response_json = EntityType.objects.values().get(entity_type_id=entity_type_id)
            return HttpResponse(result=True, message="Entity detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except (Error, EntityType.DoesNotExist, ValidationError) as e:
            return HttpResponse(result=False, message="Could not fetch entity type detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_entity_type(self, entity_type_id, entity_type_data):
        try:
            update_entity = EntityType.objects.get(entity_type_id=entity_type_id)

            if "label" in entity_type_data:
                update_entity.entity_type_label = entity_type_data.get('label')
                update_entity.save()
                return HttpResponse(result=True, message="Entity Type update success.", status=status.HTTP_200_OK)
            else:
                return HttpResponse(result=False,
                                    message="Missing required Entity Type request field - 'label'. Could not update Entity Type.",
                                    status=status.HTTP_400_BAD_REQUEST)
        except Error as e:
            return HttpResponse(result=False, message="Could not update Entity Type detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_entity_type_detail(self, entity_type_id):
        try:
            EntityType.objects.get(entity_type_id=entity_type_id).delete()
            return HttpResponse(result=True, message="Entity Type delete success.", status=status.HTTP_200_OK)
        except (Error, EntityType.DoesNotExist) as e:
            return HttpResponse(result=False, message="Could not delete Entity Type detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
