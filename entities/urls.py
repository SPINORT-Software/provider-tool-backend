from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    # ====================================================
    # Entity Type Endpoints
    # ====================================================

    # (LIST)GET/POST for entity types
    path('entity-type/', EntityTypeList.as_view()),

    # GET/UPDATE/DELETE for entity type detail
    path('entity-type/<str:entity_type_id>/', EntityTypeDetail.as_view()),

    # ====================================================
    # Attribute Set Endpoints
    # ====================================================

    # (LIST)GET/POST for attribute set
    path('attribute-set/', AttributeSetList.as_view()),

    # GET/UPDATE/DELETE for attribute set detail
    path('attribute-set/<str:attribute_set_id>/', AttributeSetDetail.as_view()),

    # GET/UPDATE/DELETE for attribute set detail
    path('attribute-set/<str:attribute_set_id>/attribute-group', AttributeSetGroups.as_view()),

    # ====================================================
    # Attribute Group Endpoints
    # ====================================================

    # (LIST)GET/POST for attribute group
    path('attribute-group/', AttributeGroupList.as_view()),

    # GET/UPDATE/DELETE for attribute group detail
    path('attribute-group/<str:attribute_group_id>/', AttributeGroupDetail.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
