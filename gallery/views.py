from django.views.generic import ListView, DetailView
from gallery.models import GalleryAlbum


class AlbumListView(ListView):
    model = GalleryAlbum
    template_name = 'gallery/index.html'
    context_object_name = 'albums'

    def get_queryset(self):
        return GalleryAlbum.objects.prefetch_related('images').order_by('title')


class AlbumDetailView(DetailView):
    model = GalleryAlbum
    template_name = 'gallery/album.html'
    context_object_name = 'album'
    queryset = GalleryAlbum.objects.prefetch_related('images')
