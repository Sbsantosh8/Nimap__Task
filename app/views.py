from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class ClientListCreateView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)

        # Customize the response structure for GET requests
        response_data = []
        for client in serializer.data:
            created_by_username = None
            if client["created_by"] is not None:
                try:
                    created_by_user = User.objects.get(
                        id=client["created_by"]
                    )  # Get the User object
                    created_by_username = created_by_user.username
                except User.DoesNotExist:
                    created_by_username = None

            response_data.append(
                {
                    "id": client["id"],
                    "client_name": client["client_name"],
                    "created_at": client["created_at"],
                    "created_by": created_by_username,
                }
            )

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save(
                created_by=request.user
            )  # Set the created_by field
            # Customize the response for the POST request
            response_data = {
                "id": client.id,
                "client_name": client.client_name,
                "created_at": client.created_at.isoformat(),  # Ensure proper ISO format
                "created_by": (
                    client.created_by.username if client.created_by else None
                ),  # Get username
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer


class ClientDetailView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        return get_object_or_404(Client, id=id)

    def get(self, request, id, *args, **kwargs):
        client = self.get_object(id)

        # Retrieve projects associated with the client
        projects = Project.objects.filter(client=client).values("id", "project_name")

        # Customize the response data
        response_data = {
            "id": client.id,
            "client_name": client.client_name,
            "projects": list(projects),  # Convert queryset to list
            "created_at": client.created_at.isoformat(),  # Ensure proper ISO format
            "created_by": (
                client.created_by.username if client.created_by else None
            ),  # Get username
            "updated_at": client.updated_at.isoformat(),  # Assuming you have an updated_at field
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        client = self.get_object(id)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            updated_client = serializer.save()
            # Customize the response for the PUT request
            response_data = {
                "id": updated_client.id,
                "client_name": updated_client.client_name,
                "created_at": updated_client.created_at.isoformat(),  # Ensure proper ISO format
                "created_by": (
                    updated_client.created_by.username
                    if updated_client.created_by
                    else None
                ),  # Get username
                "updated_at": updated_client.updated_at.isoformat(),  # Assuming you have an updated_at field
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        client = self.get_object(id)
        client_id = client.id
        client.delete()
        return Response(
            {
                "message": f"Successfully Deleted! Client Name: {client.client_name}, Client Id: {client_id}"
            },
            status=status.HTTP_204_NO_CONTENT,
        )


from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserListCreateView(APIView):
    """
    List all users or create a new user.
    """

    permission_classes = [AllowAny]  # Only authenticated users can view or create

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"success": f"User {user.username} created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import get_object_or_404


class UserDetailView(APIView):
    """
    Retrieve, update, or delete a user instance.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"success": f"User {user.username} updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(
            {"success": f"User {user.username} deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Client, User
from .serializers import ProjectSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        client_id = self.kwargs.get("id")  # Get client ID from the URL
        try:
            client = Client.objects.get(id=client_id)  # Retrieve the client
        except Client.DoesNotExist:
            return Response(
                {"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Prepare the data for the new project
        project_data = {
            "project_name": request.data.get("project_name"),
            "client": client,  # Set the client object
            "created_by": request.user,  # Assuming the request has user info
        }

        # Create the project instance
        project = Project(**project_data)

        try:
            # Save the project to generate an ID
            project.save()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If there are users to associate, handle them after saving the project
        if "users" in request.data:
            user_ids = [user["id"] for user in request.data.get("users", [])]
            users = User.objects.filter(id__in=user_ids)  # Get all users in one query

            for user_instance in users:
                project.users.add(user_instance)  # Add user to the project

        # Prepare the response data
        response_data = {
            "id": project.id,
            "project_name": project.project_name,
            "client": client.client_name,  # Use client_name instead of client object
            "users": [
                {"id": user.id, "name": user.username} for user in users
            ],  # Get user IDs and usernames
            "created_at": project.created_at,
            "created_by": project.created_by.username,  # Assuming created_by is a User object
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserProjectListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, *args, **kwargs):
        # Return projects associated with the logged-in user
        projects = Project.objects.filter(users=request.user)

        response_data = [
            {
                "id": project.id,
                "project_name": project.project_name,
                "created_at": project.created_at,
                "created_by": (
                    project.created_by.username if project.created_by else None
                ),  # Assuming created_by is a User object
            }
            for project in projects
        ]

        return Response(response_data, status=status.HTTP_200_OK)
