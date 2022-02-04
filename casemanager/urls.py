from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # Case Manager Endpoints
    # ====================================================

    # LIST for daily workload
    path('workload', WorkloadViews.WorkloadList.as_view()),

    path('<str:casemanager>/workload', WorkloadViews.WorkloadListFilterByCaseManager.as_view()),

    # ADD - EDIT - DELETE for daily workload
    path('workload/<str:pk>', WorkloadViews.WorkloadDetail.as_view()),

    path('client-assessment-create', ClientAssessmentViews.ClientAssessmentCreate.as_view()),

    # LIST for Client Assessment
    path('client-assessment', ClientAssessmentViews.ClientAssessmentList.as_view()),

    path('<str:casemanager>/client-assessment',
         ClientAssessmentViews.ClientAssessmentListFilterByCaseManager.as_view()),

    # ADD - EDIT - DELETE for Client Assessment
    path('client-assessment/<str:pk>', ClientAssessmentViews.ClientAssessmentDetail.as_view()),

    path('client-intervention', ClientInterventionViews.ClientInterventionList.as_view()),

    path('client-intervention-create', ClientInterventionViews.ClientInterventionCreate.as_view()),

    path('<str:casemanager>/client-intervention',
         ClientInterventionViews.ClientInterventionListFilterByCaseManager.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
