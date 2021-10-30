from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # Client Endpoints
    # ====================================================

    # communication Logs
    path('communication-logs', CommunicationLogs.CommunicationLogList.as_view()),
    path('communication-logs/<str:pk>/', CommunicationLogs.CommunicationLogUpdateDeleteRetrieve.as_view()),

    # Visitor Logs
    path('visitor-logs', VisitorLogs.VisitorsLogList.as_view()),
    path('visitor-logs/<str:pk>/', VisitorLogs.VisitorsLogUpdateDeleteRetrieve.as_view()),

    # Personal Information
    path('personal', PersonalInformation.PersonalInformationList.as_view()),
    path('personal-create', PersonalInformation.PersonalInformationCreate.as_view()),
    path('personal/<str:pk>/', PersonalInformation.PersonalInformationUpdateDeleteRetrieve.as_view()),

    # Clinical Information
    path('clinical', ClinicalInformation.ClinicalInformationCreate.as_view()),
    path('clinical/<str:pk>/', VisitorLogs.VisitorsLogUpdateDeleteRetrieve.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
