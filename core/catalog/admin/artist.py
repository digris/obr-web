from django.contrib import admin
from catalog.models.artist import Artist, ArtistImage
from image.admin import SortableImageInlineMixin


class ArtistImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = ArtistImage


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = [
        "name",
    ]
    inlines = [
        ArtistImageInline,
    ]
