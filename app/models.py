from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    client_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.client_name


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(
        Client, related_name="projects", on_delete=models.CASCADE
    )
    users = models.ManyToManyField(
        User, related_name="projects", blank=True
    )  # Many-to-Many relationship
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        related_name="created_projects",
        on_delete=models.CASCADE,
        default=1,  # Replace 1 with a valid user ID
    )

    def __str__(self):
        return self.project_name


class ProjectUser(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="project_users"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_projects"
    )

    class Meta:
        unique_together = (
            "project",
            "user",
        )  # Prevents duplicate entries for the same project and user

    def __str__(self):
        return f"{self.user.username} in {self.project.project_name}"
