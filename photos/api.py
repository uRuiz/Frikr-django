from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from photos.models import Photo
from photos.serializer import PhotoSerializer


class PhotoListAPI(ListCreateAPIView):
    """
    Endpoint de listado y creación de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoDetailAPI(RetrieveUpdateDestroyAPIView):
    """
    Endpoint de detalle, actualización y borrado de fotos
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer