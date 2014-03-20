import datetime
import os
from django.conf import settings

from django.db.models import (
    Model,
    ForeignKey,
    Field,
    TextField,
    CharField,
    URLField,
    BooleanField,
    DateTimeField,
    SlugField,
)

from .managers import (
    ProjectManager,
)

class Project (Model):
    SUPPORTED_LANGUAGES = (
        ("d", "D"),
    )

    active = BooleanField(
        default= False,
        help_text= "Switch this on to make the project public.",
    )

    time_updated = DateTimeField()

    name = CharField(
        max_length= 255,
        verbose_name= "Project Name",
        help_text= "Set the name for this project, for display.",
    )

    slug = SlugField(
        max_length= 255,
        help_text= "A slug for the project, used in generated output.",
    )

    language = CharField(
        max_length= 255,
        choices= SUPPORTED_LANGUAGES,
        verbose_name= "Programming Language",
        help_text= (
            "This field will be used to decide the method used "
            "for generating documentation"
        ),
    )

    source_directory= CharField(
        max_length= 65535,
        verbose_name= "Source Directory",
    )

    source_url = URLField(
        max_length= 255,
        verbose_name= "Source URL",
        help_text= "Set this to a URL for the project's source code.",
    )

    summary_line = CharField(
        max_length= 255,
    )

    description = TextField(
        default= "",
        help_text= "Input Markdown here to describe the project.",
    )

    objects = ProjectManager()

    def __str__(self):
        return self.slug

    @property
    def absolute_source_directory(self):
        """
        Get the absolute path to this project's source directory.
        """
        return os.path.abspath(os.path.join(
            settings.D_SOURCE_PARENT_DIR,
            self.source_directory,
        ))

    @property
    def import_keyword(self):
        if self.language == "d":
            return "import"
        else:
            assert False

    @property
    def line_end(self):
        if self.language == "d":
            return ";"
        else:
            assert False

    def load_documentation(self, location):
        """
        Load a documentation object for this object.

        If a document with the object does not exist, a DoesNotExist
        exception will be thrown.
        """
        if self.language == "d":
            return DDoc.objects.get(
                project= self,
                location= location,
            )
        else:
            assert False

    def extra_source_list(self):
        """
        Load extra sources for this project as a list.

        The result will be cached in this object after the first query.
        """
        if not hasattr(self, "__source_list"):
            # Cache the result.
            self.__source_list = (
                self.extra_sources.all()
                .values_list("source_directory", flat= True)
            )

        return self.__source_list

    def module_list(self):
        """
        Yield a complete module list for this project.
        """
        if self.language == "d":
            return self.ddocs.all().only("location")
        else:
            assert False

class ExtraSource (Model):
    project = ForeignKey(Project, related_name="extra_sources")

    source_directory= CharField(
        max_length= 65535,
        verbose_name= "Source Directory",
    )

class DDoc (Model):
    class Meta:
        unique_together = (
            ("project", "location"),
        )

        ordering = ("location", )

    project = ForeignKey(Project, related_name="ddocs")
    location = CharField(max_length= 255)
    html = TextField()

    @property
    def namespace(self):
        return self.location.replace("/", ".")

