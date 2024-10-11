from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add password field

    class Meta:
        model = User
        fields = ["id", "username", "password"]  # Include password in fields

    def create(self, validated_data):
        # Hash the password before saving the user
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])  # Hash the password
        user.save()  # Save the user instance
        return user


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "project_name"]


class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ["id", "client_name", "projects", "created_at", "created_by"]
        read_only_fields = ["created_at", "created_by"]

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None
