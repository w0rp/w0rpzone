from django.contrib.admin import site as admin_site

from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    TabularInline,
)

from .models import (
    Project,
    ExtraSource,
    DDoc,
)

class ExtraSourceInline (TabularInline):
    model = ExtraSource

class ProjectAdmin (ModelAdmin):
    list_display = (
        "name",
        "language",
    )

    inlines = (
        ExtraSourceInline,
    )

class DDocAdmin (ModelAdmin):
    list_display = (
        "project",
        "location",
    )

    fields = (
        "project",
        "location",
        "html",
    )

admin_site.register(Project, ProjectAdmin)
admin_site.register(DDoc, DDocAdmin)

