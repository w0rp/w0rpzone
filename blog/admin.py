from django.contrib import admin as dj_admin

from . import models

class BlogAuthorAdmin(dj_admin.ModelAdmin):
    list_display = ("author", )

class ArticleTagInline(dj_admin.StackedInline):
    model = models.ArticleTag

class ArticleFileInline(dj_admin.StackedInline):
    model = models.ArticleFile

class ArticleAdmin(dj_admin.ModelAdmin):
    list_display = ("slug", "title", "author", "creation_date")

    inlines = [
        ArticleTagInline,
        ArticleFileInline
    ]

class ArticleTagAdmin(dj_admin.ModelAdmin):
    list_display = ("tag", "article")

dj_admin.site.register(models.BlogAuthor, BlogAuthorAdmin)
dj_admin.site.register(models.Article, ArticleAdmin)
dj_admin.site.register(models.ArticleTag, ArticleTagAdmin)
dj_admin.site.register(models.ArticleFile)
dj_admin.site.register(models.ArticleComment)

