import os
import sys
import shutil
import tempfile
from optparse import make_option

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.timezone import now

from programming_projects.models import Project
from programming_projects.doc_generator.d import generate_d_doc_tasks

def check_d_settings(queryset):
    """
    Check settings for D projects for the project queryset, if any D
    projects exist.
    """
    if not queryset.filter(language= "d").exists():
        return

    if not hasattr(settings, "D_SOURCE_PARENT_DIR"):
        raise CommandError(
            "D_SOURCE_PARENT_DIR is not set in settings!"
        )

    if not hasattr(settings, "DDOC_TEMPLATE"):
        raise CommandError(
            "DDOC_TEMPLATE is not set in settings!"
        )

    if not os.path.exists(settings.DDOC_TEMPLATE):
        raise CommandError(
            "DDOC_TEMPLATE file does not exist! ({})".format(
                settings.DDOC_TEMPLATE,
            )
        )

    if not shutil.which("dmd"):
        raise CommandError(
            "dmd could not be found in your path!"
        )

def delete_previous_models(project_queryset):
    for project in project_queryset:
        if project.language == "d":
            project.ddocs.all().delete()
        else:
            assert False, "Unhandled project type: " + project.language

def generate_model_tasks(project_queryset):
    """
    Generate a sequence of tasks yielding model for generating
    documentation. The models should be saved later in the main thread.
    """
    for project in project_queryset:
        if project.language == "d":
            yield from generate_d_doc_tasks(project)
        else:
            assert False, "Unhandled project type: " + project.language

def parallel(iterator):
    """
    Given an iterator of zero argument functions, execute those
    functions in a thread pool and yield the results.
    """
    from concurrent.futures import ThreadPoolExecutor
    from multiprocessing import cpu_count

    with ThreadPoolExecutor(max_workers= cpu_count()) as executor:
        yield from executor.map(lambda f: f(), iterator)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option("--all",
            action= "store_true",
            dest= "generate_all",
            default= False,
            help= "Generate documentation for all projects."
        ),
    )

    def handle(self, *args, **options):
        if options["generate_all"]:
            queryset = Project.objects.all()
        elif len(args) > 0:
            queryset = Project.objects.filter(slug__in= args)
        else:
            raise CommandError(
                "At least one project name should be given."
            )

        if not queryset:
            raise CommandError(
                "No projects were matched."
            )

        # Writes all have to happen in the main thread,
        # this is because the DB API is not thread safe.
        with transaction.atomic():
            delete_previous_models(queryset)

            # We'll do all of the doc processing in a few different threads.
            for model in parallel(generate_model_tasks(queryset)):
                model.save()

            # Update all project 'updated' times.
            queryset.update(time_updated= now())

