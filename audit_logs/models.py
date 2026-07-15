from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("login", "Login"),
    ]


    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_logs"
    )


    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )


    module = models.CharField(
        max_length=50
    )


    description = models.TextField()


    timestamp = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            "-timestamp"
        ]


    def __str__(self):

        return (
            f"{self.user} - "
            f"{self.action} - "
            f"{self.module}"
        )