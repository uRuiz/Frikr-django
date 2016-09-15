from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from photos.models import Photo
from photos.serializers import PhotoSerializer, PhotoListSerializer


class PhotoListAPI(ListCreateAPIView):
    """
    Endpoint de listado y creación de fotos
    """
    queryset = Photo.objects.all()

    def get_serializer_class(self):
        return PhotoSerializer if self.request.method == 'POST' else PhotoListSerializer


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Endpoint de detalle, actualización y borrado de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer