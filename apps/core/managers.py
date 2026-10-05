from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        # массовое удаление через .filter().delete() тоже мягкое
        return self.update(deleted_at=timezone.now())


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # скрываем удалённые записи
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)