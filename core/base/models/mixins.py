# -*- coding: utf-8 -*-
import uuid
from django.db import models


class TimestampedModelMixin(models.Model):
    """TimestampedModelMixin
    An abstract base class model that provides self-managed "created" and
    "updated" fields.
    """

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class UUIDModelMixin(models.Model):
    """UUIDModelMixin
    An abstract base class model that provides a self-managed "uuid" field.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class CTModelMixin(models.Model):
    """CTModelMixin
    An abstract base class model that provides content-type related methods / attributes.
    """

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()

    @property
    def ct(self):
        return self.get_ct()

    class Meta:
        abstract = True


class CTUIDModelMixin(UUIDModelMixin, CTModelMixin, models.Model):
    """CTModelMixin
    An abstract base class model that provides content-type & ID related methods / attributes.
    """

    @property
    def uid(self):
        if not self.uuid:
            return None
        return str(self.uuid)[:8].upper()

    def __repr__(self):
        return f"{self.ct}:{self.uuid}"

    def __str__(self):
        return f"{self.ct}:{self.uid}"

    class Meta:
        abstract = True
