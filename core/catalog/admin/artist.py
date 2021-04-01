from django.contrib import admin
from catalog.models import Artist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    save_on_top = True
