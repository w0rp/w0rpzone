from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import (
    Project,
)

def doc_view(request, project_slug, location):
    try:
        project = Project.objects.get(slug= project_slug)
        doc = project.load_documentation(location= location)
    except ObjectDoesNotExist:
        raise Http404("Doc not found!")

    return render(request, "programming_projects/doc.dj.htm", {
        "project": project,
        "module": doc,
        "doc_body": mark_safe(doc.html),
    })

