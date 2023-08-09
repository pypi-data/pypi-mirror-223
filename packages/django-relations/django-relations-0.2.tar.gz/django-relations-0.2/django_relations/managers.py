from django.db import models
from django.db.models import ForeignKey, OneToOneField, ManyToManyField


class CustomRelatedFieldsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        related_fields = set()
        prefetch_related = set()
        for field in self.model._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneField)):
                related_fields.add(field.name)
            elif isinstance(field, ManyToManyField):
                prefetch_related.add(field.name)
        if related_fields and prefetch_related:
            return queryset.select_related(*related_fields).prefetch_related(*prefetch_related)
        elif related_fields:
            return queryset.select_related(*related_fields)
        elif prefetch_related:
            return queryset.prefetch_related(*prefetch_related)
        else:
            return queryset