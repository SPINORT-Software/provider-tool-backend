from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # External Partner Endpoints
    # ====================================================

    path('interventions/', ClientInterventionList.as_view()),

    path('<str:casemanager>/interventions', ClientInterventionListFilterByCaseManager.as_view()),

    # path('client-intervention-create', ClientInterventionViews.ClientInterventionCreate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
