from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from .views import *

urlpatterns = [
    path('entity-type/', EntityTypeList.as_view()),  # GET/POST for entity types
    path('entity-type/<int:type_id>', EntityTypeDetail.as_view()),  # UPDATE/DELETE for entity types
]

urlpatterns = format_suffix_patterns(urlpatterns)
