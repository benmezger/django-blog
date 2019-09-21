from django.db import models

from blog.queryset import CustomQuerySet


class CheckBeforeDeleteManager(models.Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)
