from django.contrib.admin import (
    ModelAdmin,
    TabularInline
)

from w0rplib.admin import register_for

from . import models

@register_for(models.Company)
class CompanyAdmin(ModelAdmin):
    list_display = ("name", )

@register_for(models.Region)
class RegionAdmin(ModelAdmin):
    list_display = ("code", "name")

class GameReleaseInline(TabularInline):
    model = models.GameRelease

@register_for(models.Game)
class GameAdmin(ModelAdmin):
    list_display = ("title", "developer")

    inlines = [
        GameReleaseInline
    ]

@register_for(models.Platform)
class PlatformAdmin(ModelAdmin):
    list_display = ("name", )

@register_for(models.GameRelease)
class GameReleaseAdmin(ModelAdmin):
    list_display = ("game", "region", "publisher", "release_date")

