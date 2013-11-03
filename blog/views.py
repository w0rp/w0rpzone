import datetime

from django.shortcuts import (
    render,
    get_object_or_404
)

from w0rplib.view import using_template

from . import models

def blog_template(base_name):
    return using_template("blog/" + base_name + ".dj.htm")

@blog_template("main")
def blog_main_page(request):
    return {
    }

@blog_template("main")
def blog_article_page(article_slug):
    import sys

    article = get_object_or_404(models.Article, slug= article_slug)

    return {
        "article" : article,
    }

