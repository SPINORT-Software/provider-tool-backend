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
    path('personal', PersonalInformationViews.PersonalInformationList.as_view()),
    path('personal-create-update', PersonalInformationViews.PersonalInformationCreate.as_view()),
    path('personal/<str:pk>/', PersonalInformationViews.PersonalInformationRetrieve.as_view()),
    path('<str:client>/personal', PersonalInformationViews.ClientPersonalInformationRetrieve.as_view()),

    # Clinical Information
    path('clinical', ClinicalInformationViews.ClinicalInformationList.as_view()),
    path('clinical-create-update', ClinicalInformationViews.ClinicalInformationCreateUpdate.as_view()),
    path('clinical/<str:pk>/', ClinicalInformationViews.ClinicalInformationRetrieve.as_view()),
    path('<str:client>/clinical', PersonalInformationViews.ClientPersonalInformationRetrieve.as_view()),

    path('<str:client_id>/profile', ClientViews.ClientProfileRetrieve.as_view()),
    path('<str:client_id>/data', ClientViews.ClientDataRetrieve.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
