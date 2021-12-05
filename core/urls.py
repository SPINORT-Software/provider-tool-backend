from django.urls import path
from .views import current_user, UserList, UserSearch, ClientSearch, ClientSearchByEmail

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('search-user', UserSearch.as_view()),
    path('search-client', ClientSearch.as_view()),
    path('search-client-email', ClientSearchByEmail.as_view())
]