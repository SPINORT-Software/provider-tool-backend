from django.shortcuts import render
from entities.models import UserEntity, UserRoleEntityData, \
    UserRoleAttribute, UserRoleAttributeValues, UserRoleEntityDataTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import Error
from entities.model import entities, attributes
from django.core.exceptions import ValidationError

"""
Create: 
    1/ entity type record.
    2/ entity data record.
    3/ entity data types. 
"""
entityModel = entities.EntityTypeModel()
attributeSetModel = attributes.AttributeSetModel()
attributeGroupModel = attributes.AttributeGroupModel()


class EntityTypeList(APIView):

    def post(self, request):
        """
        Add a new entity type record.
        :param request:
        :return:
        """
        try:
            response = entityModel.create_entity_type(request.data)
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not create entity type.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        List all the entity type records.
        :param request:
        :return:
        """
        try:
            response = entityModel.list_entity_type()
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not fetch entity types.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntityTypeDetail(APIView):
    """
    EntityType model detail - Edit/Get Detail/Delete
    """

    def put(self, request, entity_type_id):
        """
        Update the entity type detail.
        :param request:
        :param entity_type_id:
        :return:
        """
        try:
            response = entityModel.update_entity_type(entity_type_id, request.data)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not update entity type detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, entity_type_id):
        """
        Get Entity type detail
        :param request:
        :param entity_type_id:
        :return:
        """
        try:
            response = entityModel.get_entity_type_detail(entity_type_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not fetch entity type detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, entity_type_id):
        """
        Require additional permission/access to delete EntityType record.
        :param entity_type_id:
        :param request:
        :return:
        """
        try:
            response = entityModel.delete_entity_type_detail(entity_type_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not delete entity type detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EntityList(APIView):
    """
    Create or List entity records by record type
    """
    pass


class EntityDetail(APIView):
    """
    Edit/delete an entity record of any type.
    """
    pass


class EntityDataList(APIView):
    """
    List or add data to an entity record (*_entity_data records)
    """
    pass


class EntityDataDetail(APIView):
    """
    Edit/delete all *__entity_data records.
    """
    pass


class EntityDataTypeList(APIView):
    """
    List or add Entity data types
    """
    pass


class EntityDataTypeDetail(APIView):
    """
    Edit/delete entity data types
    """
    pass


class AttributeSetList(APIView):
    def post(self, request):
        try:
            response = attributeSetModel.create_attribute_set(request.data)
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not create Attribute Set.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            response = attributeSetModel.list_attribute_set()
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not list Attribute Set.'
            }, status=status.HTTP_400_BAD_REQUEST)


class AttributeSetDetail(APIView):
    def put(self, request, attribute_set_id):
        """
        Update the attribute set detail.
        :param request:
        :param attribute_set_id:
        :return:
        """
        try:
            response = attributeSetModel.update_attribute_set(attribute_set_id, request.data)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not update attribute set detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, attribute_set_id):
        """
        Get Attribute Set detail
        :param request:
        :param attribute_set_id:
        :return:
        """
        try:
            response = attributeSetModel.get_attribute_set_detail(attribute_set_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not fetch attribute set detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, attribute_set_id):
        """
        Require additional permission/access to delete Attribute Set record.
        :param attribute_set_id:
        :param request:
        :return:
        """
        try:
            response = attributeSetModel.delete_attribute_set_detail(attribute_set_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not delete attribute set detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttributeSetGroups(APIView):
    def get(self, request, attribute_set_id):
        """
        Get Attribute Groups by AttributeSet ID
        :param request:
        :param attribute_set_id:
        :return:
        """
        try:
            response = attributeSetModel.get_attribute_set_groups(attribute_set_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not fetch attribute set groups.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttributeGroupList(APIView):
    def post(self, request):
        try:
            response = attributeGroupModel.create_attribute_group(request.data)
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not create Attribute Group.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            response = attributeGroupModel.list_attribute_group()
            return response.get_response()
        except Error:
            return Response({
                'result': False,
                'message': 'Could not list Attribute Group.'
            }, status=status.HTTP_400_BAD_REQUEST)


class AttributeGroupDetail(APIView):
    def get(self, request, attribute_group_id):
        """
        Get Attribute Group detail
        :param request:
        :param attribute_group_id:
        :return:
        """
        try:
            response = attributeGroupModel.get_attribute_group_detail(attribute_group_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not fetch attribute group detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, attribute_group_id):
        """
        Update the attribute group detail.
        :param request:
        :param attribute_group_id:
        :return:
        """
        try:
            response = attributeGroupModel.update_attribute_group(attribute_group_id, request.data)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not update attribute group detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, attribute_group_id):
        """
        Require additional permission/access to delete AttributeGroup record.
        :param attribute_set_id:
        :param request:
        :return:
        """
        try:
            response = attributeGroupModel.delete_attribute_group_detail(attribute_group_id)
            return response.get_response()
        except (Error, ValidationError):
            return Response({
                'result': False,
                'message': 'Could not delete attribute group detail.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
