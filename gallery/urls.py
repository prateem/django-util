from django.urls import path
from gallery.views import AlbumListView, AlbumDetailView

app_name = 'gallery'

urlpatterns = [
    path('', AlbumListView.as_view(), name='index'),
    path('<slug:slug>/', AlbumDetailView.as_view(), name='album')
]
