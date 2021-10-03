from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # Case Manager Endpoints
    # ====================================================

    # LIST for daily workload
    path('workload', WorkloadList.as_view()),

    # ADD - EDIT - DELETE for daily workload
    path('workload/<str:pk>', WorkloadDetail.as_view()),

    # LIST for Client Assessment
    path('client-assessment', ClientAssessmentList.as_view()),

    path('client-assessment-create', ClientAssessmentCreate.as_view()),

    # ADD - EDIT - DELETE for Client Assessment
    path('client-assessment/<str:pk>', ClientAssessmentDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
