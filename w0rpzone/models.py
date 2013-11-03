import os.path
import time

from django.db import models as dj_model
from django.contrib.auth.models import User

class Blog(dj_model.Model):
    """
    A blog, which contains articles, etc.
    """
    slug = dj_model.SlugField(max_length=255)
    title = dj_model.CharField(max_length=255)
    description = dj_model.TextField()

class BlogAuthor(dj_model.Model):
    """
    A blog author.
    """
    blog = dj_model.ForeignKey(Blog)
    author = dj_model.ForeignKey(User)

    class Meta:
        unique_together = ("blog", "author")

class Article(dj_model.Model):
    """
    An article on a blog.
    """
    blog = dj_model.ForeignKey(Blog)
    author = dj_model.ForeignKey(User)
    creation_date = dj_model.DateField(auto_now_add=True)
    slug = dj_model.SlugField(max_length=255)
    title = dj_model.CharField(max_length=255)
    content = dj_model.TextField()

class ArticleTag(dj_model.Model):
    """
    A tag for a blog article.
    """
    article = dj_model.ForeignKey(Aritcle)
    # The tag is indexed for fast lookup.
    tag = dj_model.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ("article", "tag")

def file_extension(filename):
    """
    Get the file extension including the leading dot for a filename.

    Examples
    =========
    "file.jpg" -> ".jpg"
    "file.tar.gz" -> ".tar.gz"
    "file" -> ""
    """
    split = filename.split(".")

    if len(split) == 1:
        return ""

    return "." + ".".join(split[1:])

def article_file_path(article, filename):
    return "upload/article/{}/{:d}{}".format(
        aritcle.slug,
        int(time.time() * 1000),
        file_extension(filename)
    )

class AritcleFile(dj_model.Model):
    """
    A file uploaded for an article.
    """
    article = dj_model.ForeignKey(Aritcle)
    file = dj_model.FileField(upload_to=article_file_path)

class ArticleComment(dj_model.Model):
    """
    A comment on an article.
    """
    article = dj_model.ForeignKey(Aritcle)
    creation_date = dj_model.DateField(auto_now_add=True)
    poster_name = dj_model.CharField(max_length=255)
    content = dj_model.TextField()

