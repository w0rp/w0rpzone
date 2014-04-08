from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.utils.safestring import mark_safe

from .models import (
    Project,
)

load_project = Project.objects.load_project


def project_list_view(request):
    projects = (
        Project.objects.
        active_projects_for_user(request.user)
        .order_by("name")
    )

    if not projects.exists():
        raise Http404("No projects found!")

    return render(request, "programming_projects/list.dj.htm", {
        "projects": projects,
    })


def project_summary_view(request, project_slug):
    try:
        project = load_project(request.user, project_slug)
    except ObjectDoesNotExist:
        raise Http404("Project does not exist!")

    return render(request, "programming_projects/summary.dj.htm", {
        "project": project,
    })


def doc_view(request, project_slug, location):
    try:
        project = load_project(request.user, project_slug)
        doc = project.load_documentation(location=location)
    except ObjectDoesNotExist:
        raise Http404("Doc not found!")

    return render(request, "programming_projects/doc.dj.htm", {
        "project": project,
        "module": doc,
        "doc_body": mark_safe(doc.html),
    })
