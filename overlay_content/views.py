from __future__ import print_function
import os

from django.shortcuts import render
from django.http import HttpResponse

class AlbumImage(object):
    def __init__(self, filename, caption):
        super(AlbumImage, self).__init__()

        self.filename = filename
        self.caption = caption

def overlay(request):
    # TODO Return templated page with rotating set of images
    # TODO Get now playing
    # TODO Display now playing to screen
    # TODO Currently making tab
    # TODO Past work link
    # TODO Say hello text

    # Get list of images in folder
    base_path = os.path.join('D:\\', 'Django', 'overlay', 'overlay_content', 'static', 'overlay_content', 'test_album')
    image_names = os.listdir(base_path)[0:2]

    context = {'images': [AlbumImage('overlay_content/test_album/' + x, 'Thing') for x in image_names]}
    return render(request, 'overlay_content/overlay_content.html', context)
