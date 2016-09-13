from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.list import ListView
from django.urls import reverse

from photos.forms import PhotoForm
from photos.models import Photo, VISIBILITY_PUBLIC


class HomeView(View):

    def get(self, request):
        """
        Renderiza el home con un listado de fotos
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        # recupera todas las fotos de la base de datos
        photos = Photo.objects.filter(visibility=VISIBILITY_PUBLIC).order_by('-created_at')
        context = {'photos_list': photos[:4]}
        return render(request, 'photos/home.html', context)


class PhotoDetailView(View):

    def get(self, request, pk):
        """
        Renderiza el detalle de una imagen
        :param request: objeto HttpRequest con los datos de la petición
        :param pk: clave primaria de la foto a recuperar
        :return: objeto HttpResponse con los datos de la respuesta
        """
        possible_photos = Photo.objects.filter(pk=pk).select_related("owner")
        if len(possible_photos) == 0:
            return HttpResponseNotFound("La imagen que buscas no existe")
        elif len(possible_photos) > 1:
            return HttpResponse("Múltiples opciones", status=300)

        photo = possible_photos[0]
        context = {'photo': photo}
        return render(request, 'photos/photo_detail.html', context)


class PhotoCreationView(View):

    @method_decorator(login_required())
    def get(self, request):
        """
        Presenta el formulario para crear una foto
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        message = None
        photo_form = PhotoForm()
        context = {'form': photo_form, 'message': message}
        return render(request, 'photos/photo_creation.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
        Presenta el formulario para crear una foto y en caso de que la petición sea POST la valida
        y la crea en caso de que sea válida
        :param request: objeto HttpRequest con los datos de la petición
        :return: objeto HttpResponse con los datos de la respuesta
        """
        message = None
        photo_with_user = Photo(owner=request.user)
        photo_form = PhotoForm(request.POST, instance=photo_with_user)
        if photo_form.is_valid():
            new_photo = photo_form.save()
            photo_form = PhotoForm()
            message = 'Foto creada satisfactoriamente <a href="{0}">Ver foto</a>'.format(
                reverse('photos_detail', args=[new_photo.pk])
            )

        context = {'form': photo_form, 'message': message}
        return render(request, 'photos/photo_creation.html', context)


class PhotoListView(LoginRequiredMixin, ListView):

    model = Photo
    template_name = 'photos/photo_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
