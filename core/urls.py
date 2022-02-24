from django.urls import path
from .views import UserSearch, ClientSearch, ClientSearchByEmail, ApplicationUserView

urlpatterns = [
    path('search-user', UserSearch.as_view()),

    path('search-client', ClientSearch.as_view()),

    path('search-client-email', ClientSearchByEmail.as_view()),

    path('search-app-users', ApplicationUserView.as_view()),
]
