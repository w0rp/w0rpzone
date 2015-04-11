import time
import datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse as url_reverse
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import (
    Model,
    ForeignKey,
    OneToOneField,
    TextField,
    CharField,
    BooleanField,
    DateTimeField,
    SlugField,
    FileField,
    GenericIPAddressField,
)

from .managers import (
    ArticleManager,
    CommenterManager,
)


class BlogAuthor(Model):
    """
    Users which can edit the blog posts.
    """
    author = OneToOneField(User)

    class Meta:
        # Tables are named explicitly to make direct SQL more predictable.
        db_table = "blog_blogauthor"

    def __str__(self):
        return str(self.author)


class Article(Model):
    """
    An article on the blog.
    """
    class Meta:
        db_table = "blog_article"
        ordering = ["-creation_date"]
        index_together = (
            ("creation_date", "active"),
        )

    author = ForeignKey(User)
    active = BooleanField(default=False)
    creation_date = DateTimeField()
    slug = SlugField(max_length=55)
    title = CharField(max_length=55)
    content = TextField()

    objects = ArticleManager()

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

        ArticleTag.objects.bulk_create([
            ArticleTag(article=self, tag=tag)
            for tag in
            set(tag_seq)
        ])


class ArticleTag(Model):
    """
    A tag for a blog article.
    """
    class Meta:
        db_table = "blog_articletag"
        unique_together = ("article", "tag")

    article = ForeignKey(Article, related_name="tags")
    # The tag is indexed for fast lookup.
    tag = CharField(max_length=255, db_index=True)

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
        article.slug,
        int(time.time() * 1000),
        file_extension(filename)
    )


class ArticleFile(Model):
    """
    A file uploaded for an article.
    """
    class Meta:
        db_table = "blog_articlefile"

    article = ForeignKey(Article)
    file = FileField(upload_to=article_file_path)


class Commenter(Model):
    ip_address = GenericIPAddressField(unique=True)
    time_banned = DateTimeField(null=True, blank=True)

    objects = CommenterManager()

    def __str__(self):
        return self.ip_address if self.ip_address is not None else "NULL"

    @property
    def is_banned(self):
        """
        Return True if this commenter has been banned.
        """
        return bool(self.pk and self.time_banned is not None)

    def last_comment_time_or_none(self):
        """
        Return the last creation date for all comments tied to this object.

        This time is None when the commenter doesn't yet exist in the database
        or no comments exist for the commenter.
        """
        if not self.pk:
            return None

        try:
            latest_comment = (
                self.comments
                .only("creation_date")
                .latest()
            )

            return latest_comment.creation_date
        except ObjectDoesNotExist:
            return None

    def is_comment_too_soon(self, timestamp):
        """
        Return True if this commenter is making another comment too soon.
        """
        assert isinstance(timestamp, datetime.datetime)

        last_post_time = self.last_comment_time_or_none()

        return (
            last_post_time is not None
            and (timestamp - last_post_time).total_seconds() < 30
        )


class ArticleComment(Model):
    """
    A comment on an article.
    """
    DEFAULT_NAME = "Anonymous"

    class Meta:
        db_table = "blog_articlecomment"
        ordering = ["creation_date"]
        get_latest_by = "creation_date"

    commenter = ForeignKey(Commenter, related_name="comments")
    article = ForeignKey(Article, related_name="comments")
    creation_date = DateTimeField(auto_now_add=True)
    poster_name = CharField(
        verbose_name="Name",
        max_length=255,
        blank=True,
    )
    content = TextField(
        verbose_name="Comment",
    )

    def __str__(self):
        return "{}/{} - {}".format(
            self.commenter,
            self.poster_name,
            self.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @property
    def poster_name_or_default(self):
        """
        Return either the name the poster set or the DEFAULT_NAME
        """
        return (
            self.poster_name
            if self.poster_name.strip() else
            self.DEFAULT_NAME
        )
