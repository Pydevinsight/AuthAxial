import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


# Create your models here.

class DeletableManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by('created').filter(deleted=False)


class Datation(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deleted = models.BooleanField(default=False, editable=False)
    objects = DeletableManager()
    h_objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def delete(self):
        self.deleted = True
        return super().save()

    def hard_delete(self):
        """
        Physically delete from the DB
        :return:
        """
        return super().delete()

    def copy(self, save=False):
        """
        Create a copy of the existing object
        by unsetting it pk a returning the object
        :return:
        """
        _obj = self
        _obj.pk = None
        if save:
            _obj.save()
        return _obj
