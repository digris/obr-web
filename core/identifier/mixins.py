from django.db import models


class IdentifierModelMixin(models.Model):
    class Meta:
        abstract = True
