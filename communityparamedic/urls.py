from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # Community Paramedic Endpoints
    # ====================================================

    # LIST for daily workload
    path('workload', WorkloadList.as_view()),

    # ADD - EDIT - DELETE for daily workload
    path('workload/<str:pk>', WorkloadDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
