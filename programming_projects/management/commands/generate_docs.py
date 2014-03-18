import os
import sys
import shutil
import subprocess
import tempfile
from itertools import chain

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from programming_projects.models import (
    Project,
    DDoc,
)

class SettingsException(Exception):
    pass

def find_d_files(project):
    """
    Given a Project, which defines a source directory, yield
    pairs of (full_path_to_file, module_path)
    """
    top_dir = project.absolute_source_directory

    for root, _, filename_list in os.walk(top_dir):
        for filename in filename_list:
            extension_length = 0

            if filename.endswith(".d"):
                extension_length = 2
            elif filename.endswith(".di"):
                extension_length = 3

            if extension_length == 0:
                continue

            full_filename = os.path.join(root, filename)
            module_location = full_filename[
                len(top_dir) + 1 : -extension_length
            ]

            if os.path.sep != "/":
                # On operating systems like say, Windows, force
                # this into being / here.
                module_location = module_location.replace(
                    os.path.sep, "/"
                )

            yield (full_filename, module_location)

def prepare_dmd_commandline(project):
    """
    Build a DMD commandline without the sources specified.
    """
    return tuple(chain(
        (
            "dmd",
            # Don't generate object code.
            "-o-",
            # Include this source path.
            "-I" + project.absolute_source_directory,
        ),
        (
            "-I" + os.path.join(
                settings.D_SOURCE_PARENT_DIR,
                extra_source_directory
            )
            for extra_source_directory in
            project.extra_source_list()
        ),
        (
            settings.DDOC_TEMPLATE,
        )
    ))

def generate_ddoc_html(project, dmd_commandline, source_filename):
    """
    Given a project, a previously prepared DMD commandline, and a
    source filename, generate DDoc HTML for that source file.

    The resulting HTML will be returned.
    """
    temp_filename = tempfile.mkstemp()[1]

    try:
        command = tuple(chain(
            dmd_commandline,
            (
                # Write the doc to this temporary file.
                "-Df" + temp_filename,
                # Generate the doc from this source filename.
                source_filename,
            )
        ))

        # TODO: Raise errors from DMD here.
        subprocess.check_call(command)

        with open(temp_filename) as html_file:
            return html_file.read()
    finally:
        # We must check if the file exists.
        # Exceptions *can* remove it before we do.
        if os.path.isfile(temp_filename):
            os.remove(temp_filename)

def generate_d_docs(project):
    """
    Generate all DDocs for a project and store them in the database.

    All previously created DDocs will be deleted.
    """
    dmd_commandline = prepare_dmd_commandline(project)

    with transaction.atomic():
        # Delete all current DDocs.
        project.ddocs.all().delete()

        # Create them again.
        for filename, module_path in find_d_files(project):
            DDoc(
                project= project,
                location= module_path,
                html= generate_ddoc_html(project, dmd_commandline, filename)
            ).save()

def generate_d_projects():
    """
    Generate documentation for every D project the site knows about.
    """
    d_projects = Project.objects.filter(language= "d")

    if not d_projects:
        return

    if not hasattr(settings, "D_SOURCE_PARENT_DIR"):
        raise SettingsException(
            "D_SOURCE_PARENT_DIR is not set in settings!"
        )

    if not hasattr(settings, "DDOC_TEMPLATE"):
        raise SettingsException(
            "DDOC_TEMPLATE is not set in settings!"
        )

    if not os.path.exists(settings.DDOC_TEMPLATE):
        raise SettingsException(
            "DDOC_TEMPLATE file does not exist! ({})".format(
                settings.DDOC_TEMPLATE,
            )
        )

    if not shutil.which("dmd"):
        raise SettingsException(
            "dmd could not be found in your path!"
        )

    for project in d_projects:
        generate_d_docs(project)

def generate_everything():
    """
    Generate documentation for every single type of programming
    project on the site.
    """
    try:
        generate_d_projects()
    except SettingsException as err:
        sys.stderr.write(str(err))
        sys.stderr.write("\nD documentation will not be generated!\n")

class Command(BaseCommand):
    def handle(self, *args, **options):
        generate_everything()
