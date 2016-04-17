import os

from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.staticfiles import finders


def view_presentation(request, filename):
    # Find the file in staticfiles.
    full_path = finders.find(os.path.join("presentation", filename + ".htm"))

    if not os.path.exists(full_path):
        return HttpResponseNotFound("Unknown presentation name: " + filename)

    with open(full_path) as presentation_file:
        presentation_html = presentation_file.read()

    return render(request, "presentation/view.dj.htm", {
        "presentation_html": presentation_html,
    })
