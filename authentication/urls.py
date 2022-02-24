from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, UserView

app_name = 'authentication'
urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
    path('users/login', LoginAPIView.as_view()),
    path('user/profile', UserView.as_view()),
]
