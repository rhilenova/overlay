from __future__ import print_function
import os

from django.shortcuts import render
from django.http import HttpResponse

class AlbumImage(object):
    def __init__(self, filename, caption):
        super(AlbumImage, self).__init__()

        self.filename = filename
        self.caption = caption

# TODO base_path as arg?
# TODO config for base_path
def get_images():
    # Get list of images in folder
    base_path = os.path.join('D:\\', 'Django', 'overlay', 'overlay_content', 'static', 'overlay_content', 'test_album')
    image_names = os.listdir(base_path)
    if len(image_names) >= 50:
        raise RuntimeError('Too many images in album. Max is 49. Album has %d' % (len(image_names)))

    return image_names

def overlay(request):
    # TODO Get now playing
    # TODO Display now playing to screen
    # TODO Currently making tab
    # TODO Past work link
    # TODO Say hello text

    image_names = get_images()

    # Return templated page with rotating set of images
    context = {'images': [AlbumImage('overlay_content/test_album/' + x, 'Thing') for x in image_names]}
    return render(request, 'overlay_content/overlay_content.html', context)

def overlay_css(request):
    image_names = get_images()
    context = {'images': [AlbumImage('overlay_content/test_album/' + x, 'Thing') for x in image_names]}
    return render(request, 'overlay_content/overlay_content.css', context)
