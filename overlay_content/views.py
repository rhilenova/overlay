from __future__ import print_function
import os
import textwrap

from django.shortcuts import render
from django.http import HttpResponse

def overlay(request):
    # Return templated page with rotating set of images
    return render(request, 'overlay_content/overlay_content.html', {})

def overlay_css(request):
    return render(request, 'overlay_content/overlay_content.css', {})
