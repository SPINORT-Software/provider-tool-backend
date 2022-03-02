from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from .views import *

urlpatterns = [
    path('communication', SharerViews.ShareListCreateView.as_view()),
    path('communication/<str:application_user_id>', SharerViews.ShareListCreateView.as_view()),

    path('referrals', SharerViews.ReferralListView.as_view()),
    path('referrals/<str:type>', SharerViews.ReferralListViewFilterByType.as_view()),
    path('followups', SharerViews.FollowUpListView.as_view()),
    path('followups/<str:type>', SharerViews.FollowUpListViewFilterByType.as_view()),

    path('notifications', SharerViews.NotificationsListView.as_view()),
    path('notifications/all', SharerViews.NotificationsListAllView.as_view()),

    path('notifications/<str:pk>/read', SharerViews.NotificationsRead.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
