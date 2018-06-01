from django.contrib import admin
from django.utils.html import format_html
from gallery.models import GalleryAlbum, GalleryImage


class GridInline(admin.options.InlineModelAdmin):
    template = 'gallery/admin/edit_inline/grid.html'


class ImagesInline(GridInline):
    model = GalleryImage
    extra = 3
    exclude = ('width', 'height', 'thumbnail')
    readonly_fields = ('preview', 'uploaded',)

    # Does not work. obj is the Album (parent), not the Image (formset/child) that it should be.
    # -> Bug, see: https://code.djangoproject.com/ticket/15602
    # def get_fields(self, request, obj=None):
    #     fields = ['title', 'file', 'preview', 'uploaded']
    #     if obj is None:
    #         fields.remove('preview')
    #         fields.remove('uploaded')
    #     return tuple(fields)

    @staticmethod
    def preview(image):
        if image.id:
            return format_html("<img src='{}' width='{}' height='{}'>",
                               image.thumbnail.url, image.thumbnail.width, image.thumbnail.height)
        return "-"


@admin.register(GalleryAlbum)
class AlbumAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title', 'description']}),
    ]
    list_display = ('title', 'description', 'image_count')
    inlines = [ImagesInline]

    def image_count(self, album):
        return album.images.count()
    image_count.short_description = 'Images'
