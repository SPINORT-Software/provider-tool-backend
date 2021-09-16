from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import Roles, RolePermissions, UserRoleEntityDataTypes
from django.db.utils import IntegrityError, DatabaseError, Error
from django.core.exceptions import ValidationError
from providertool.constants import *


class RolesModel:
    """
    Perform all Roles CRUD operations.
    """

    def list_roles(self):
        """
        List all Roles records.
        :return:
        """
        try:
            response_json = Roles.objects.values()

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Roles list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=True, message="No roles found.",
                                status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Failed to list Roles.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_role(self, role_data):
        """
        Create a Role record.
        :param role_data:
        :return:
        """
        try:
            if all(key not in role_data for key in API_ROLE_CREATE_REQUEST_BODY):
                return HttpResponse(result=False, message="Missing required request field values.",
                                    status=status.HTTP_400_BAD_REQUEST)

            role_created = Roles()
            role_created.role_code = role_data.get("code")
            role_created.role_label = role_data.get("label")
            role_created.save()

            return HttpResponse(result=True, message="Role record created.",
                                status=status.HTTP_200_OK,
                                id_value=role_created.role_id,
                                id="role_id")

        except IntegrityError as ie:
            ie_message = ie.args[1]
            if "Duplicate entry" in ie_message:
                ie_message = "The role code already exists. Failed to create role record."

            return HttpResponse(result=False, message=ie_message,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_role_detail(self, role_id):
        """
        Get Roles detail.
        :param role_id:
        :return:
        """
        try:
            response_json = Roles.objects.values().get(role_id=role_id)
            return HttpResponse(result=True, message="Role detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except ValidationError:
            return HttpResponse(result=False, message="Invalid role query parameter provided.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except (Error, Roles.DoesNotExist) as e:
            return HttpResponse(result=False, message="Failed to fetch Role detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_role_detail(self, role_id, role_data):
        try:
            update_role = Roles.objects.get(role_id=role_id)

            if "label" in role_data:
                update_role.role_label = role_data.get('label')

            update_role.save()
            return HttpResponse(result=True, message="Role detail update success.", status=status.HTTP_200_OK)
        except ValidationError:
            return HttpResponse(result=False, message="Invalid role query parameter provided.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Error as e:
            return HttpResponse(result=False, message="Failed to update role detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_role_data_types(self, role_id):
        """
        List all entity data types (sections) filtered by role.
        :param role_id:
        :return:
        """
        try:
            permission_resources = RolePermissions.objects.select_related('role_id', 'resource').filter(
                role_id=role_id).order_by('resource').values_list('resource').distinct()

            data_types = UserRoleEntityDataTypes.objects.values().filter(entity_data_type_id__in=permission_resources)

            if len(data_types) > 0:
                return HttpResponse(result=True, message="Data types list generated successfully.",
                                    status=status.HTTP_200_OK, value=data_types)

            return HttpResponse(result=False, message="No Data types found.",
                                status=status.HTTP_200_OK)

        except Error as e:
            return HttpResponse(result=False, message="Failure to list data types.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RolesPermissionModel:
    def add_role_permission(self, role_data):
        """
        Create a Role Permissions record.
        :param role_data:
        :return:
        """
        try:
            if all(key not in role_data for key in API_ROLE_PERMISSION_CREATE_REQUEST_BODY):
                return HttpResponse(result=False, message="Missing required request field values.",
                                    status=status.HTTP_400_BAD_REQUEST)

            if role_data.get("resource_type") not in ALLOWED_PERMISSION_RESOURCE_TYPES:
                return HttpResponse(result=False, message="Invalid resource type value provided.",
                                    status=status.HTTP_400_BAD_REQUEST)

            operation_type = role_data.get("operation_type").upper()
            if operation_type not in ALLOWED_PERMISSION_OPERATION_TYPES:
                return HttpResponse(result=False, message="Invalid operation type value provided.",
                                    status=status.HTTP_400_BAD_REQUEST)

            role_permission_created = RolePermissions()

            role_permission_created.role_id = Roles.objects.get(role_id=role_data.get("role_id"))
            role_permission_created.operation_type = operation_type
            role_permission_created.resource_type = role_data.get("resource_type")
            role_permission_created.resource_id = role_data.get("resource_id")
            role_permission_created.save()

            return HttpResponse(result=True, message="Role permission record created.",
                                status=status.HTTP_200_OK, id_value=role_permission_created.permission_id,
                                id="permission_id")

        except Roles.DoesNotExist:
            return HttpResponse(result=False, message="Invalid role value provided.",
                                status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError as ie:
            ie_message = ie.args[1]
            if "Duplicate entry" in ie_message:
                ie_message = "Failed to create role permission record. Permission for the resource-operation-role already exists."

            return HttpResponse(result=False, message=ie_message,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_role_permission(self):
        """
        List all RolePermissions objects.
        :return:
        """
        try:
            response_json = RolePermissions.objects.values()

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Role permission list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=True, message="No role permissions found.",
                                status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Failed to list role permissions.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_role_permission_by_role(self, role_id):
        """
        List all RolePermissions objects by role_id.
        :return:
        """
        try:
            response_json = RolePermissions.objects.values().filter(role_id=role_id)

            if len(response_json) > 0:
                return HttpResponse(result=True, message="Role permission list by role generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)

            return HttpResponse(result=True, message="No role permissions found for provided role.",
                                status=status.HTTP_200_OK)
        except RolePermissions.DoesNotExist:
            return HttpResponse(result=False, message="Failed to list role permissions for provided role.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Error as e:
            return HttpResponse(result=False, message="Failed to list role permissions for provided role.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_detail(self, role_permission_id):
        try:
            response_json = RolePermissions.objects.values().get(permission_id=role_permission_id)
            return HttpResponse(result=True, message="Role Permission detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except ValidationError:
            return HttpResponse(result=False, message="Invalid role permission query parameter provided.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except RolePermissions.DoesNotExist:
            return HttpResponse(result=False, message="Role permission record does not exist.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Error as e:
            return HttpResponse(result=False, message="Failed to fetch Role permission detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, role_permission_id):
        try:
            RolePermissions.objects.get(permission_id=role_permission_id).delete()
            return HttpResponse(result=True, message="Role permission deletion success.", status=status.HTTP_200_OK)
        except RolePermissions.DoesNotExist:
            return HttpResponse(result=False, message="Role permission record does not exist.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Error as e:
            return HttpResponse(result=False, message="Failed to delete Role permissions.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
