from django.urls import path
from .views import (
    ClientListCreateView,
    ClientDetailView,
    ProjectCreateView,
    UserProjectListView,
    UserListCreateView,
    UserDetailView,
)

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path("clients/", ClientListCreateView.as_view(), name="client-list"),
    path("clients/<int:id>/", ClientDetailView.as_view(), name="client-detail"),
    path(
        "clients/<int:id>/projects/", ProjectCreateView.as_view(), name="project-create"
    ),
    path("projects/", UserProjectListView.as_view(), name="user-projects"),
    # path("createuser/", CreateUserView.as_view(), name="create-user"),
    path("users/", UserListCreateView.as_view(), name="user-list-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
