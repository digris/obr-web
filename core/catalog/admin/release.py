from django.contrib import admin
from catalog.models.release import Release, ReleaseImage
from image.admin import SortableImageInlineMixin


class MediaArtistInline(admin.TabularInline):
    model = Release.media.through
    raw_id_fields = ["media"]
    extra = 0


class ReleaseImageInline(SortableImageInlineMixin, admin.TabularInline):
    model = ReleaseImage


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [
        MediaArtistInline,
        ReleaseImageInline,
    ]
