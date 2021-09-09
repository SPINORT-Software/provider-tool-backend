from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    # ======================================================
    # User Entity Data Records
    # ======================================================
    path('data', UserEntityDataList.as_view()),
    path('data/<str:user_id>', UserEntityDataListByUser.as_view()),

    # ======================================================
    # User Entity Data Types
    # ======================================================
    path('data-types', UserEntityDataTypesList.as_view()),
    path('data-types/<str:type_id>/detail', UserEntityDataTypesDetail.as_view()),
    path('data-type/<str:type_id>/attributes', UserEntityAttributesListDataType.as_view()),

    # ======================================================
    # User Entity Attributes
    # ======================================================
    path('attributes', UserEntityAttributesList.as_view()),
    path('attributes/<str:attribute_id>/detail', UserEntityAttributesDetail.as_view()),

    # ======================================================
    # User Entity Attribute Values
    # ======================================================
    path('attribute-values', UserEntityAttributeValues.as_view()),

    # ======================================================
    # User Entity Attribute Group
    # Get a list of attributes in an Attribute Group.
    # ======================================================
    path('attribute-group/<str:attr_group_id>/attributes', UserEntityAttributesListAttrGroup.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
