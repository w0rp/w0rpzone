import re
import os
import subprocess
import tempfile
import subprocess

from itertools import chain
from functools import partial

from django.conf import settings
from django.db import transaction

import lxml.html

from programming_projects.models import (
    Project,
    DDoc,
)

THIS_SPACE_RE = re.compile(r"> +this")
CONSTRAINT_RE = re.compile(r"(if \(.*\))")

def post_process_ddoc(html):
    root = lxml.html.fromstring(html)

    for elem in root.find_class("declaration"):
        # Get an HTML string for the element.
        elem_string = lxml.html.tostring(elem).decode("utf-8")

        # Correct some extra whitespace.
        elem_string = re.sub(
            THIS_SPACE_RE,
            r'>this',
            elem_string
        )

        # Wrap template constraints in spans so we can style them, etc.
        elem_string = re.sub(
            CONSTRAINT_RE,
            r'<span class="template_constraint">\1</span>',
            elem_string
        )

        # Replace the element instead with the string we created.
        parent = elem.getparent()
        parent.insert(parent.index(elem), lxml.html.fromstring(elem_string))
        parent.remove(elem)

    for elem in root.find_class("definition"):
        # Remove all definitions which are blank.
        if elem.text_content().isspace():
            elem.getparent().remove(elem)

    return lxml.html.tostring(root)

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
            return post_process_ddoc(html_file.read())
    finally:
        # We must check if the file exists.
        # Exceptions *can* remove it before we do.
        if os.path.isfile(temp_filename):
            os.remove(temp_filename)

def generate_d_doc_tasks(project):
    """
    Generate a bunch of tasks each yield DDoc models for saving
    documentation in the database.
    """
    dmd_commandline = prepare_dmd_commandline(project)

    def doc_worker(filename, module_path):
        return DDoc(
            project= project,
            location= module_path,
            html= generate_ddoc_html(project, dmd_commandline, filename)
        )

    yield from (partial(doc_worker, *args) for args in find_d_files(project))
