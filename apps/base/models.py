import uuid

from django.db import models
from django.contrib.auth.models import User


class AbstractBaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_%(class)s",
        editable=False,
        blank=True,
        null=True
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="update_%(class)s",
        editable=False,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True