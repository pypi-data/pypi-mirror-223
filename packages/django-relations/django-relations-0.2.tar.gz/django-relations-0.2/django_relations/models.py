from django.db import models
from .managers import CustomRelatedFieldsManager


class AbstractDefaultClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    objects = CustomRelatedFieldsManager()

    class Meta:
        abstract = True
