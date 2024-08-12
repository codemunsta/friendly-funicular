import uuid

from django.db import models


class ModelCreation(models.Model):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)  # noqa: A003
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
