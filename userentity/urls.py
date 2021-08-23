from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path('data-types', UserEntityDataTypesList.as_view()),
    path('data-types/<str:type_id>', UserEntityDataTypesDetail.as_view()),

    path('userentity-attributes', UserEntityAttributes.as_view()),
    path('userentity-values', UserEntityAttributeValues.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
