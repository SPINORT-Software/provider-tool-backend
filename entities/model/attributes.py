from rest_framework.response import Response
from entities.helper import HttpResponse
from rest_framework import status
from entities.models import AttributeSet, AttributeGroup
from django.db.utils import IntegrityError, DatabaseError, Error
import uuid
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict


class AttributeSetModel:
    """
    AttributeSet Model:
        All CRUD operations of AttributeSet model.
    """

    def create_attribute_set(self, attribute_set_data):
        """
        Create attribute set record.
        :param attribute_set_data:
        :return:
        """
        try:
            attribute_set_created = AttributeSet()
            if all(key in attribute_set_data for key in ("name", "code")):
                attribute_set_created.attribute_set_name = attribute_set_data.get("name")
                attribute_set_created.attribute_set_code = attribute_set_data.get("code")
                attribute_set_created.save()

                attribute_group_data = {'name': "default__" + attribute_set_data.get("code"),
                                        'code': "default__" + attribute_set_data.get("code"), 'is_default_group': True,
                                        'set_id': attribute_set_created.attribute_set_id}

                attribute_group_model = AttributeGroupModel()
                attribute_group_model.create_attribute_group(attribute_group_data=attribute_group_data)

                return HttpResponse(result=True, message="Attribute set creation success.", status=status.HTTP_200_OK,
                                    id="Attribute Set ID",
                                    id_value=attribute_set_created.attribute_set_id)
            else:
                return HttpResponse(result=True, message="Missing required attribute set request values.",
                                    status=status.HTTP_400_BAD_REQUEST)
        except Error as e:
            return HttpResponse(result=False, message=f"Could not create attribute set. [{e.args[1]}]",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_attribute_set(self):
        """
        List all attribute set records.
        :return:
        """
        try:
            response_json = AttributeSet.objects.values()
            if len(response_json) > 0:
                return HttpResponse(result=True, message="Attribute Set list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)
            else:
                return HttpResponse(result=True, message="No Attribute Set found.",
                                    status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Could not list Attribute Set values.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_attribute_set(self, attribute_set_id, attribute_set_data):
        try:
            update_attribute_set = AttributeSet.objects.get(attribute_set_id=attribute_set_id)

            if "name" in attribute_set_data:
                update_attribute_set.attribute_set_name = attribute_set_data.get('name')
                update_attribute_set.save()
            else:
                return HttpResponse(result=False,
                                    message="Missing required Attribute Set request field - 'name'. Could not update "
                                            "Attribute Set",
                                    status=status.HTTP_400_BAD_REQUEST)
            return HttpResponse(result=True, message="Attribute Set update success.", status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Could not update Attribute Set detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_attribute_set_detail(self, attribute_set_id):
        """
        Get AttributeSet detail.
        :param attribute_set_id:
        :return:
        """
        try:
            response_json = AttributeSet.objects.values().get(attribute_set_id=attribute_set_id)
            return HttpResponse(result=True, message="Attribute Set detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except (Error, AttributeSet.DoesNotExist, ValidationError) as e:
            return HttpResponse(result=False, message=f"Could not fetch Attribute Set detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_attribute_set_detail(self, attribute_set_id):
        try:
            AttributeSet.objects.get(attribute_set_id=attribute_set_id).delete()
            return HttpResponse(result=True, message="Attribute Set delete success.", status=status.HTTP_200_OK)
        except (Error, AttributeSet.DoesNotExist) as e:
            print(e)
            return HttpResponse(result=True, message="Could not delete Attribute Set.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_attribute_set_groups(self, attribute_set_id):
        """
        List all attribute group records by AttributeSet ID
        :return:
        """
        try:
            response_json = AttributeGroup.objects.filter(attribute_set_id__attribute_set_id=attribute_set_id).values()
            if len(response_json) > 0:
                return HttpResponse(result=True, message="Attribute Set - Groups list generated successfully.",
                                    status=status.HTTP_200_OK,
                                    value=response_json)
            else:
                return HttpResponse(result=True, message="No Attribute Set Groups found.",
                                    status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Could not list Attribute Set - Groups.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AttributeGroupModel:
    """
    AttributeGroup Model:
    All CRUD operations of AttributeGroup model.
    """

    def create_attribute_group(self, attribute_group_data):
        """
        Create attribute group record.
        :param attribute_group_data:
        :return:
        """
        try:
            attribute_group_created = AttributeGroup()

            if all(key in attribute_group_data for key in ("name", "code", "set_id")):
                set_id = attribute_group_data.get("set_id")
                attribute_group_created.attribute_group_name = attribute_group_data.get("name")
                attribute_group_created.attribute_group_code = attribute_group_data.get("code")
                attribute_group_created.attribute_set_id = AttributeSet.objects.get(
                    attribute_set_id=set_id)

                if "is_default_group" in attribute_group_data and attribute_group_data.get("is_default_group"):
                    attribute_group_created.is_default_group = True

                attribute_group_created.save()
                return HttpResponse(result=True, message="Attribute group creation success.", status=status.HTTP_200_OK,
                                    id="Attribute Group ID",
                                    id_value=attribute_group_created.attribute_group_id)
            else:
                return HttpResponse(result=True, message="Missing required attribute group request values.",
                                    status=status.HTTP_400_BAD_REQUEST)
        except AttributeSet.DoesNotExist:
            return HttpResponse(result=False,
                                message="Could not map Attribute Set value. Please provide a valid attribute set value.",
                                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return HttpResponse(result=False,
                                message="Please provide a valid attribute set value.",
                                status=status.HTTP_400_BAD_REQUEST)
        except Error as e:
            return HttpResponse(result=False, message=f"Could not create attribute group. [{e.args[1]}]",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list_attribute_group(self):
        """
        List all attribute group records.
        :return:
        """
        try:
            response_json = AttributeGroup.objects.values()
            return HttpResponse(result=True, message="Attribute Group list generated successfully.",
                                status=status.HTTP_200_OK,
                                value=response_json)
        except Error as e:
            return HttpResponse(result=False, message="Could not list Attribute Group values.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update_attribute_group(self, attribute_group_id, attribute_group_data):
        """
        Update AttributeGroup model record.
        :param attribute_group_id:
        :param attribute_group_data:
        :return:
        """
        try:
            update_attribute_group = AttributeGroup.objects.get(attribute_group_id=attribute_group_id)

            if "name" in attribute_group_data:
                update_attribute_group.attribute_group_name = attribute_group_data.get('name')
            if "set_id" in attribute_group_data:
                update_attribute_group.attribute_set_id = AttributeSet.objects.get(
                    attribute_set_id=attribute_group_data.get("set_id"))
            update_attribute_group.save()
            return HttpResponse(result=True, message="Attribute Group update success.", status=status.HTTP_200_OK)
        except Error as e:
            return HttpResponse(result=False, message="Could not update Attribute Group detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_attribute_group_detail(self, attribute_group_id):
        """
        Get AttributeGroup detail.
        :param attribute_group_id:
        :return:
        """
        try:
            attribute_group = AttributeGroup.objects.get(attribute_group_id=attribute_group_id)
            response_json = model_to_dict(attribute_group)
            response_json['attribute_set'] = model_to_dict(attribute_group.attribute_set_id)
            return HttpResponse(result=True, message="Attribute Group detail fetch success.", status=status.HTTP_200_OK,
                                value=response_json)
        except (Error, AttributeGroup.DoesNotExist, ValidationError) as e:
            return HttpResponse(result=False, message=f"Could not fetch Attribute Group detail.",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
