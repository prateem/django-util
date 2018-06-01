# Requires Pillow python package
from PIL import Image
from io import BytesIO
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from django_util.mixins.slugged_model_mixin import SluggedMixin
import os

THUMBNAIL_MAX_SIZE = (300, 300)


# The upload and thumbnail directories will both be inside the settings.MEDIA_ROOT directory.
def get_upload_directory(instance, filename):
    return "gallery/%(album)s/%(fn)s" % {'album': instance.album.slug, 'fn': filename}


def get_thumbnail_directory(instance, filename):
    upload_dir = get_upload_directory(instance, filename)
    return "%(upload_to)s/thumbnails/%(fn)s" % {'upload_to': upload_dir[:-len(filename)], 'fn': filename}


class GalleryAlbum(SluggedMixin, models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=60)
    slug = models.CharField(verbose_name=_('Slug'), max_length=60)
    description = models.CharField(verbose_name=_('Description'), max_length=100, blank=True, default=None)

    def __str__(self):
        return self.title

    def get_cover_image(self) -> 'GalleryImage':
        return self.images.first()

    class Meta:
        verbose_name = _('Album')


class GalleryImage(models.Model):
    @staticmethod
    def image_pre_save(sender, instance: 'GalleryImage', **kwargs):
        try:
            original = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            # newly uploaded. thumbnail should be generated.
            instance.set_thumbnail()
        else:
            if not original.image == instance.image:
                # modified. thumbnail should be re-generated.
                instance.set_thumbnail()

    title = models.CharField(verbose_name=_('Title'), max_length=60, blank=True)
    image = models.ImageField(verbose_name=_('Image'), upload_to=get_upload_directory,
                              width_field='width', height_field='height')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    thumbnail = models.ImageField(verbose_name=_('Thumbnail'), upload_to=get_thumbnail_directory)
    uploaded = models.DateField(verbose_name=_('Date Uploaded'), default=timezone.now)
    album = models.ForeignKey(to='GalleryAlbum', verbose_name=_('Album'),
                              on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return "%(title)s (%(width)d x %(height)d)" % {
            'title': self.title or "Untitled",
            'width': self.width,
            'height': self.height
        }

    def set_thumbnail(self):
        img = Image.open(self.image)
        img.thumbnail(THUMBNAIL_MAX_SIZE, Image.LANCZOS)

        img_name, img_ext = os.path.splitext(self.image.name)
        img_ext = img_ext.lower()
        thumb_fn = "%(img_name)s_thumbnail%(ext)s" % {'img_name': img_name, 'ext': img_ext}

        thumb_io = BytesIO()
        img.save(thumb_io, img.format)
        thumb_io.seek(0)

        self.thumbnail.save(thumb_fn, ContentFile(thumb_io.read()), save=False)
        thumb_io.close()

    class Meta:
        verbose_name = _('Image')


pre_save.connect(GalleryImage.image_pre_save, sender=GalleryImage)
