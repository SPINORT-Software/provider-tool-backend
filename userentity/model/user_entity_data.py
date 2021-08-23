from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import UserRoleEntityDataTypes, UserRoleEntityData, UserRoleAttribute, AttributeGroup
from django.db.utils import IntegrityError, DatabaseError, Error
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from providertool.constants import *
from datetime import datetime


class UserEntityDataTypesModel:
    def add_type(self, type_data):
        """
        Create a user entity data type record.
        :param type_data:
        :return:
        """
        try:
            if all(key not in type_data for key in API_ENTITY_DATA_TYPES_CREATE_REQUEST_BODY):
                return HttpResponse(result=False, message="Missing required request field values for entity data type.",
                                    status=status.HTTP_400_BAD_REQUEST)

            data_type_created = UserRoleEntityDataTypes()
            data_type_created.data_type_code = type_data.get("data_type_code")
            data_type_created.data_type_label = type_data.get("data_type_label")
            data_type_created.save()

            return HttpResponse(result=True, message="Created User Entity Data type",
                                status=status.HTTP_200_OK, id_value=data_type_created.entity_data_type_id,
                                id="data_type_id")

        except IntegrityError as ie:
            ie_message = ie.args[1]
            if "Duplicate entry" in ie_message:
                ie_message = "The data type 'code' already exists. Could not create entity data type record."
            return HttpResponse(result=False, message=ie_message,
                                status=status.HTTP_400_BAD_REQUEST)

        except Error as e:
            return HttpResponse(result=False, message="Failed to created data type",
                                status=status.HTTP_400_BAD_REQUEST)

    def get_type_detail(self, data_type_id):
        try:
            response_json = UserRoleEntityDataTypes.objects.values().get(entity_data_type_id=data_type_id)
            return HttpResponse(result=True, message="Data type detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except ValidationError:
            return HttpResponse(result=False, message="Invalid data type query parameter provided.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except UserRoleEntityDataTypes.DoesNotExist as e:
            return HttpResponse(result=False, message="Data type detail does not exist.",
                                status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Failure to fetch Data type detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_data_types(self):
        try:
            response_json = UserRoleEntityDataTypes.objects.values()

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Data types list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=False, message="No Data types found.",
                                status=status.HTTP_200_OK)

        except Error as e:
            return HttpResponse(result=False, message="Failure to list data types.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_type_detail(self, data_type_id, data_type_detail):
        """
        Update Entity Data type detail
        Only permitted to update data_type_label, is_active, updated_at values.
        Not allowed to update data_type_code.
        :param data_type_id:
        :param data_type_detail:
        :return:
        """
        try:
            update_data_type = UserRoleEntityDataTypes.objects.get(entity_data_type_id=data_type_id)

            for attr, val in data_type_detail.items():
                if attr in API_ENTITY_DATA_TYPES_UPDATE_REQUEST_BODY:
                    setattr(update_data_type, attr, val)

            update_data_type.updated_at = datetime.now()
            update_data_type.save()
            return HttpResponse(result=True, message="Entity Data type detail update success.",
                                status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Failure to update entity data type detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserEntityDataAttributesModel:

    def add_attribute(self, attribute_data):
        """
        Create a user entity attribute.
        :param attribute_data:
        :return:
        """
        try:
            if all(key not in attribute_data for key in API_ENTITY_ATTRIBUTE_CREATE_REQUEST_BODY):
                return HttpResponse(result=False, message="Missing required request field values for entity data type.",
                                    status=status.HTTP_400_BAD_REQUEST)

            attribute_created = UserRoleAttribute()
            attribute_created.attribute_code = attribute_data.get("attribute_code")
            attribute_created.attribute_type = attribute_data.get("attribute_type")
            attribute_created.frontend_label = attribute_data.get("frontend_label")
            attribute_created.frontend_input = attribute_data.get("frontend_input")
            attribute_created.is_required = attribute_data.get("is_required")
            attribute_created.note = attribute_data.get("note")
            attribute_created.is_active = True
            attribute_created.attribute_group = AttributeGroup.objects.get(
                attribute_group_id=attribute_data.get("attribute_group"))

            attribute_created.save()

            return HttpResponse(result=True, message="Created User Entity Data Attribute",
                                status=status.HTTP_200_OK, id_value=attribute_created.attribute_id,
                                id="attribute_id")

        except IntegrityError as ie:
            ie_message = ie.args[1]
            if "Duplicate entry" in ie_message:
                ie_message = "The data attribute 'code' already exists. Could not create entity data attribute record."
            return HttpResponse(result=False, message=ie_message,
                                status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as ve:
            return HttpResponse(result=False,
                                message="Please provide a valid attribute group value.",
                                status=status.HTTP_400_BAD_REQUEST)

        except AttributeGroup.DoesNotExist:
            return HttpResponse(result=False,
                                message="Invalid Attribute group value. Please provide a valid attribute group value to create attribute.",
                                status=status.HTTP_400_BAD_REQUEST)

        except Error as e:
            return HttpResponse(result=False, message="Failed to created entity data attribute",
                                status=status.HTTP_400_BAD_REQUEST)

    def list_attributes(self):
        try:
            response_json = UserRoleAttribute.objects.values()

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Attribute list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=False, message="No Attributes found.",
                                status=status.HTTP_200_OK)

        except Error as e:
            return HttpResponse(result=False, message="Failure to list attributes.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_attributes_by_attr_group(self, attr_group_id):
        try:
            response_json = UserRoleAttribute.objects.values().filter(attribute_group=attr_group_id)

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Attribute list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=False, message="No Attributes found.",
                                status=status.HTTP_200_OK)

        except ValidationError as ve:
            return HttpResponse(result=False,
                                message="Please provide a valid attribute group value.",
                                status=status.HTTP_400_BAD_REQUEST)

        except AttributeGroup.DoesNotExist:
            return HttpResponse(result=False,
                                message="Invalid Attribute group value provided.",
                                status=status.HTTP_400_BAD_REQUEST)

        except Error as e:
            return HttpResponse(result=False, message="Failure to list attributes.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_attribute_detail(self, attribute_id):
        try:
            response_json = UserRoleAttribute.objects.values().get(attribute_id=attribute_id)
            return HttpResponse(result=True, message="Attribute detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except ValidationError:
            return HttpResponse(result=False, message="Invalid attribute query parameter provided.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except UserRoleAttribute.DoesNotExist as e:
            return HttpResponse(result=False, message="Attribute detail does not exist.",
                                status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Failure to fetch attribute detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_attribute(self, attribute_id, attribute_data):
        """
        Update User role entity attribute record.
        Only allowed to update frontend_label, note,
        :param attribute_id:
        :param attribute_data:
        :return:
        """
        try:
            update_attribute = UserRoleAttribute.objects.get(attribute_id=attribute_id)

            for attr, val in attribute_data.items():
                if attr in API_ENTITY_ATTRIBUTE_UPDATE_REQUEST_BODY:
                    setattr(update_attribute, attr, val)

            update_attribute.updated_at = datetime.now()
            update_attribute.save()
            return HttpResponse(result=True, message="Entity Data Attribute detail update success.",
                                status=status.HTTP_200_OK)

        except ValidationError as ve:
            return HttpResponse(result=False,
                                message="Please provide a valid attribute query value.",
                                status=status.HTTP_400_BAD_REQUEST)

        except UserRoleAttribute.DoesNotExist:
            return HttpResponse(result=False,
                                message="Invalid Attribute ID value. Please provide a valid attribute group value to update",
                                status=status.HTTP_400_BAD_REQUEST)

        except Error as e:
            return HttpResponse(result=False, message="Failure to update entity data attribute detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
