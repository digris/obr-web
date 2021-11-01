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


class UIDModelMixin(UUIDModelMixin):
    """UIDModelMixin
    An abstract base class model that provides a self-managed "uid" field.
    Requires UUIDModelMixin.
    """

    uid = models.CharField(
        max_length=8,
        editable=False,
        unique=True,
        db_index=True,
        null=True,
    )

    def get_uid(self):
        return str(self.uuid)[:8].upper()

    class Meta:
        abstract = True

    # pylint: disable=signature-differs
    def save(self, *args, **kwargs):
        self.uid = self.get_uid()
        super().save(*args, **kwargs)


class CTModelMixin(models.Model):
    """CTModelMixin
    An abstract base class model that provides content-type related methods / attributes.
    """

    def get_ct(self):
        return "{}.{}".format(self._meta.app_label, self.__class__.__name__).lower()

    @property
    def ct(self):
        return self.get_ct()

    @property
    def ct_app(self):
        return self.get_ct().split(".", maxsplit=1)[0]

    @property
    def ct_model(self):
        return self.get_ct().split(".")[1]

    class Meta:
        abstract = True


class CTUIDModelMixin(UIDModelMixin, CTModelMixin, models.Model):
    """CTModelMixin
    An abstract base class model that provides content-type & ID related methods / attributes.
    """

    # @property
    # def uid(self):
    #     if not self.uuid:
    #         return None
    #     return str(self.uuid)[:8].upper()

    def __repr__(self):
        return f"{self.ct}:{self.uuid}"

    def __str__(self):
        return f"{self.ct}:{self.uid}"

    @property
    def ct_uid(self):
        return f"{self.ct}:{self.uid}"

    class Meta:
        abstract = True
