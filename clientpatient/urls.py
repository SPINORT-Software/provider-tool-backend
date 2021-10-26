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
]

urlpatterns = format_suffix_patterns(urlpatterns)
