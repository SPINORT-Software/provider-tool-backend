from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    # ====================================================
    # Review Board Endpoints
    # ====================================================

    # LIST for Client Assessment
    path('referral', ClientReferralList.as_view()),

    path('referral/<str:pk>', ClientReferralRetrieveView.as_view()),

    path('<str:pk>/referral', ClientReferralListUserFilter.as_view()),

    path('referral-create', ClientReferralCreate.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
