from django.utils import timezone
from django.forms import (
    ValidationError,
    ModelForm,
    CharField,
    HiddenInput,
)

from .models import (
    Article,
    ArticleComment,
    Upload,
)

HONEYPOT_STRING = str(347 * 347)


def honeypot_ok(cleaned_data, missing_name):
    return (
        cleaned_data.get("verify") == HONEYPOT_STRING
        and not cleaned_data.get(missing_name)
    )


class ArticleForm(ModelForm):
    error_css_class = "error"

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
                .values_list("tag", flat=True)
            )


class EditArticleForm (ArticleForm):
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

    def save(self):
        article = super().save()

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

    title = CharField(
        required=False,
        widget=HiddenInput(attrs={"class": "ningen"}),
    )
    verify = CharField(widget=HiddenInput())

    error_css_class = "error"

    def clean(self):
        cleaned_data = super().clean()

        commenter = self.instance.commenter

        if not honeypot_ok(cleaned_data, "title"):
            raise ValidationError("You are probably a spammer.")

        if commenter.is_banned:
            raise ValidationError("You have been banned from posting.")

        if commenter.is_comment_too_soon(timezone.now()):
            raise ValidationError("You cannot comment again so soon.")

        return cleaned_data


class UploadForm (ModelForm):
    class Meta:
        model = Upload
        fields = ("file",)

    error_css_class = "error"
