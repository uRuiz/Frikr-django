# -*- coding: utf-8 -*-
from photos.models import Photo
from django.forms import ModelForm


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        exclude = ['owner']
