from django.shortcuts import render
from entities.models import UserEntity, UserRoleEntityData, \
    UserRoleAttribute, UserRoleAttributeValues, UserRoleEntityDataTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import Error
from entities.model import entities

"""
Create: 
    1/ entity type record.
    2/ entity data record.
    3/ entity data types. 
"""
entityModel = entities.EntityTypeModel()


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
                'message': 'Missing required request fields.'
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
    pass


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
