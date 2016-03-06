from html import escape as html_escape

from django.contrib.admin import site as admin_site
from django.utils import timezone

from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
)

from .models import (
    Article,
    ArticleTag,
    Commenter,
    ArticleComment,
)


class ArticleTagInline (StackedInline):
    model = ArticleTag


class ArticleCommentInline (StackedInline):
    model = ArticleComment


class ArticleAdmin (ModelAdmin):
    list_display = (
        "slug",
        "title",
        "author",
        "creation_date",
    )

    inlines = [
        ArticleTagInline,
        ArticleCommentInline,
    ]


class ArticleTagAdmin (ModelAdmin):
    list_display = (
        "tag",
        "article",
    )


class CommenterAdmin (ModelAdmin):
    actions = (
        "ban_all",
        "unban_all",
    )

    list_display = (
        "ip_address",
        "time_banned",
    )

    def ban_all(self, request, queryset):
        """
        Issue a ban for all unbanned commenters.
        """
        (
            queryset
            .filter(time_banned__isnull=True)
            .update(time_banned=timezone.now())
        )

    ban_all.short_description = "Ban all selected commenters."

    def unban_all(self, request, queryset):
        """
        Unban all commenters.
        """
        queryset.update(time_banned=None)

    unban_all.short_description = "Unban all selected commenters."


class ArticleCommentAdmin (ModelAdmin):
    fields = (
        "commenter_link",
        "article",
        "poster_name",
        "content",
    )

    readonly_fields = (
        "commenter_link",
        "article",
    )

    list_display = (
        "article",
        "poster_name",
        "creation_date",
    )

    def commenter_link(self, obj):
        if obj is None or not obj.pk:
            return "(None)"

        return '<a href="/admin/blog/commenter/{}/">{}</a>'.format(
            obj.commenter.pk,
            html_escape(obj.commenter.ip_address),
        )

    commenter_link.short_description = "Commenter"
    commenter_link.allow_tags = True

admin_site.register(Article, ArticleAdmin)
admin_site.register(ArticleTag, ArticleTagAdmin)
admin_site.register(Commenter, CommenterAdmin)
admin_site.register(ArticleComment, ArticleCommentAdmin)
