from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path('data-types', UserEntityDataTypesList.as_view()),
    path('data-types/<str:type_id>', UserEntityDataTypesDetail.as_view()),

    path('attributes', UserEntityAttributesList.as_view()),
    path('attributes/<str:attribute_id>', UserEntityAttributesDetail.as_view()),
    path('attributes/attribute-group/<str:attr_group_id>', UserEntityAttributesListAttrGroup.as_view()),
    path('attributes/data-type/<str:type_id>', UserEntityAttributesListDataType.as_view()),

    path('data', UserEntityDataList.as_view()),
    path('data/<str:user_id>', UserEntityDataListByUser.as_view()),

    path('attribute-values', UserEntityAttributeValues.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
