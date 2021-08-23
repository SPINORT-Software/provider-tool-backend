from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .model import user_entity_data


class UserEntity(APIView):
    def __init__(self):
        self.user_entity_data = user_entity_data.UserEntityDataTypesModel()
        self.user_entity_attributes = user_entity_data.UserEntityDataAttributesModel()


class UserEntityDataTypesList(UserEntity):
    def post(self, request):
        """
        Add a user entity data type.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.add_type(request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to add user entity data type.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        List all the user entity data types.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.list_data_types()
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch list of user entity data types'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityDataTypesDetail(UserEntity):
    def get(self, request, type_id):
        """
        Get user entity data type detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.get_type_detail(type_id)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch data type detail.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, type_id):
        """
        Update user entity data type detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_data.update_type_detail(type_id, request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to update data type detail.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityAttributesList(UserEntity):
    def post(self, request):
        """
        Add a user entity data attribute.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_attributes.add_attribute(request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to add user entity attribute.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        List all the user entity data attribute.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_attributes.list_attributes()
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch list of user entity data attributes'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityAttributesListAttrGroup(UserEntity):
    def get(self, request, attr_group_id):
        """
        List all the user entity data attribute by attribute group ID.
        :param request:
        :return:
        """
        try:
            response = self.user_entity_attributes.list_attributes_by_attr_group(attr_group_id)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch list of user entity data attributes'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityAttributesDetail(UserEntity):
    def get(self, request, attribute_id):
        """
        Get user entity data attribute detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_attributes.get_attribute_detail(attribute_id)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to fetch attribute detail.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, attribute_id):
        """
        Update user entity data attribute detail.
        :param type_id:
        :param request:
        :return:
        """
        try:
            response = self.user_entity_attributes.update_attribute(attribute_id, request.data)
            return response.get_response()
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to update attribute detail.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserEntityAttributeValues(UserEntity):
    pass
