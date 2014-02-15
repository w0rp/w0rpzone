import datetime

from django import forms as dj_form

from django.forms import (
    CharField,
    HiddenInput,
)

from django.core.exceptions import ValidationError

from w0rplib.form import ModelForm

from .models import (
    Article,
    ArticleComment,
)

class ArticleForm(ModelForm):
    tags = CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        article = kwargs.get("instance")

        # Set the initial value for the tags field with the space-separated
        # tags for the article.
        if isinstance(article, Article):
            self.fields["tags"].initial = " ".join(
                article.tags.all()
                .order_by("tag")
                .values_list("tag", flat= True)
            )

class NewArticleForm(ArticleForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "slug",
            "content",
            "tags",
            "active",
        )

    def save(self, author=None):
        article = super().save(commit=False)

        if author is not None:
            article.author = author

        article.creation_date = datetime.datetime.utcnow()

        article.save()

        # Now use all of the tags set to replace the tags.
        article.replace_all_tags(self.cleaned_data["tags"].split())

        return article

class EditArticleForm(ArticleForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "slug",
            "content",
            "creation_date",
            "tags",
            "active",
        )

    def save(self, author=None):
        article = super().save(commit=False)

        if author is not None:
            article.author = author

        article.save()

        # Now use all of the tags set to replace the tags.
        article.replace_all_tags(self.cleaned_data["tags"].split())

        return article

class ArticleCommentForm (ModelForm):
    class Meta:
        model = ArticleComment
        fields = (
            "poster_name",
            "content",
        )

