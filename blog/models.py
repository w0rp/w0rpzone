import os.path
import time

from django.db import models as dj_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as url_reverse

class BlogAuthor(dj_model.Model):
    """
    Users which can edit the blog posts.
    """
    author = dj_model.ForeignKey(User, unique=True)

    class Meta:
        # Tables are named explicitly to make direct SQL more predictable.
        db_table = "blog_blogauthor"

    def __str__(self):
        return str(self.author)

class Article(dj_model.Model):
    """
    An article on the blog.
    """
    author = dj_model.ForeignKey(User)
    creation_date = dj_model.DateTimeField()
    slug = dj_model.SlugField(max_length=255, unique=True)
    title = dj_model.CharField(max_length=255)
    content = dj_model.TextField()

    class Meta:
        db_table = "blog_article"
        ordering = ["-creation_date"]

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return url_reverse("article-detail", args=(self.slug,))

    def replace_all_tags(self, tag_seq):
        """
        Replace all tags for an article object with a given sequence of tags.

        Duplicates will be ignored. Tags not in the sequence will be removed.
        """
        ArticleTag.objects.filter(article=self).delete()

        for tag in tag_seq:
            tag_obj, created = ArticleTag.objects.get_or_create(
                article= self,
                tag= tag.lower(),
            )

            if created:
                tag_obj.save()

    def tags(self):
        """
        Generate all tags set for the article, in ascending order.
        """
        return (
            x["tag"] for x in (
                ArticleTag.objects.filter(article= self)
                .order_by("tag")
                .values("tag")
            )
        )

class ArticleTag(dj_model.Model):
    """
    A tag for a blog article.
    """
    article = dj_model.ForeignKey(Article)
    # The tag is indexed for fast lookup.
    tag = dj_model.CharField(max_length=255, db_index=True)

    class Meta:
        db_table = "blog_articletag"
        unique_together = ("article", "tag")

    def __str__(self):
        return "{} - {}".format(self.tag, self.article)

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

class ArticleFile(dj_model.Model):
    """
    A file uploaded for an article.
    """
    article = dj_model.ForeignKey(Article)
    file = dj_model.FileField(upload_to=article_file_path)

    class Meta:
        db_table = "blog_articlefile"

class ArticleComment(dj_model.Model):
    """
    A comment on an article.
    """
    article = dj_model.ForeignKey(Article)
    creation_date = dj_model.DateTimeField(auto_now_add=True)
    poster_name = dj_model.CharField(max_length=255)
    content = dj_model.TextField()

    class Meta:
        db_table = "blog_articlecomment"

