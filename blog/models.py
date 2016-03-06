import datetime
import time

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse as url_reverse
from django.db.models import (
    BooleanField,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    GenericIPAddressField,
    Model,
    SlugField,
    TextField,
)
from django.utils.functional import cached_property
from django.utils.html import urlize

from w0rplib.templatetags.markdown import markdown, unsafe_markdown

from .managers import ArticleManager


class TimestampModel(Model):
    """
    A model providing ``creation_date`` and ``modified_date`` fields for
    the time an object was created and modified.

    The ``save`` method has been overridden to take a special keyword argument
    ``timestamp``. If set to ``False``, the modified_date will be left
    unchanged.
    """
    class Meta:
        abstract = True

    creation_date = DateTimeField(default=timezone.now)
    modified_date = DateTimeField()

    def save(self, *args, **kwargs):
        if kwargs.pop('timestamp', True):
            self.modified_date = timezone.now()

        return super().save(*args, **kwargs)


class ContentMixin:
    """
    A mixin which takes produces cached HTML output for a model from
    the ``content`` field. The ``pk`` and ``modified_date`` will be used
    to differentiate the cache.

    A method ``compile_content`` must be defined for producing the compiled
    content when the cache is missed.
    """
    @cached_property
    def html_content(self):
        key = "{}.content{}-{}".format(
            self._meta.db_table,
            self.pk,
            time.mktime(self.modified_date.timetuple())
        )

        value = cache.get(key)

        if value is None:
            value = self.compile_content(self.content)

            cache.set(key, value)

        return value


class Article(TimestampModel, ContentMixin):
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
    slug = SlugField(max_length=55)
    title = CharField(max_length=55)
    content = TextField()

    objects = ArticleManager()

    def __str__(self):
        return str(self.slug)

    def get_absolute_url(self):
        return url_reverse("article-detail", args=(self.slug,))

    def edit_url(self):
        return url_reverse("edit-article", args=(self.slug,))

    def delete_url(self):
        return url_reverse("delete-article", args=(self.slug,))

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

    def compile_content(self, content):
        return unsafe_markdown(content)


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


class Upload(Model):
    """
    This model represents an upload for the site.
    """
    class Meta:
        db_table = "blog_upload"

    author = ForeignKey(User)
    file = FileField(upload_to="%Y-%m-%dT%H:%M:%SZ/")


class Commenter(Model):
    ip_address = GenericIPAddressField(unique=True)
    time_banned = DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.ip_address)

    def ban_url(self, article):
        return url_reverse("ban-commenter", args=(article.slug, self.id))

    def unban_url(self, article):
        return url_reverse("unban-commenter", args=(article.slug, self.id))

    @property
    def is_banned(self):
        """
        Return True if this commenter has been banned.
        """
        return bool(self.pk and self.time_banned is not None)

    def is_comment_too_soon(self, timestamp):
        """
        Return True if this commenter is making another comment too soon.
        """
        assert isinstance(timestamp, datetime.datetime)

        last_post_time = (
            (
                self.comments
                .order_by("creation_date")
                .values_list("creation_date", flat=True)
                .last()
            )
            if self.pk else
            None
        )

        return (
            last_post_time is not None
            and (timestamp - last_post_time).total_seconds() < 30
        )


class ArticleComment(TimestampModel, ContentMixin):
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
    poster_name = CharField(
        verbose_name="Name",
        max_length=255,
        blank=True,
        default=DEFAULT_NAME,
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

    def get_absolute_url(self):
        """
        Return A URL pointing to this comment on an article page.
        """
        return "{}#comment_{}".format(self.article.get_absolute_url(), self.id)

    def delete_url(self):
        return url_reverse("delete-comment", args=(self.article.slug, self.id))

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

    def compile_content(self, content):
        return urlize(markdown(content))
