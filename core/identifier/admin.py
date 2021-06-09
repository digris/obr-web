# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Identifier


class IdentifierInline(GenericTabularInline):
    model = Identifier
    extra = 0


@admin.register(Identifier)
class IdentifierAdmin(admin.ModelAdmin):
    pass
