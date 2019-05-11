from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_admins
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse as url_reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import MonthArchiveView
from django.views.generic.edit import DeleteView

from .forms import ArticleCommentForm, EditArticleForm, UploadForm
from .models import Article, ArticleComment, Commenter


def view_decorator(*args):
    return method_decorator(args, name="dispatch")


def response_403(request):  # pragma: no cover
    return render(request, "403.html", {}, status=403)


class NavigationMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["article_months"] = Article.objects.active_months()

        return context


class ArticleListMixin:
    queryset = (
        Article.objects.all()
        .filter(active=True)
        .defer("content")
        .select_related("author")
    )

    context_object_name = "article_list"


class ArticlePageView (ArticleListMixin, ListView, NavigationMixin):
    template_name = "blog/page.dj.htm"
    paginate_by = 10


class ArticleEditPageView(ListView):
    queryset = Article.objects.all().defer("content")
    context_object_name = "article_list"
    template_name = "blog/article_edit_list.dj.htm"
    paginate_by = 20


def notify_for_new_comment(comment):
    """
    Notify admins by email when a new comment is received.
    """
    mail_admins(
        subject="New Comment",
        message="\n".join((
            "A new comment has been posted.",
            "",
            "Article: {}".format(comment.article.title),
            "Link: {}{}".format(
                settings.EXTERNAL_SITE_URL,
                comment.get_absolute_url()
            ),
            "Name: {}".format(comment.poster_name_or_default),
            "",
            "-" * 79,
            "",
            comment.content
        ))
    )


class ArticleDetailView(UpdateView):
    """
    A view for looking at articles, which also supports submitting comments
    to articles.
    """
    model = ArticleComment
    form_class = ArticleCommentForm
    template_name = "blog/detail.dj.htm"

    def get_object(self):
        self.article = get_object_or_404(
            Article.objects.select_related("author"),
            slug=self.kwargs["slug"]
        )

        ip_address = (
            self.request.META.get('HTTP_X_FORWARDED_FOR')
            or self.request.META["REMOTE_ADDR"]
        )

        if self.request.method == 'POST':
            commenter, _ = Commenter.objects.get_or_create(
                ip_hash=Commenter.hash_ip(ip_address),
            )
        else:
            commenter = None

        return self.model(article=self.article, commenter=commenter)

    def get_success_url(self):
        # Redirect away to make it hard to accidentally submit twice.
        return url_reverse(
            "article-comment-bounce",
            args=[self.article.slug],
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["article"] = self.article
        data["article_months"] = Article.objects.active_months()
        data["comment_form"] = data.pop("form")

        return data

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            notify_for_new_comment(form.instance)
        except SMTPException:
            # Allow email sending to fail.
            pass

        return response


class RelatedArticleObjectMixin:
    def get_success_url(self):
        return self.article.get_absolute_url()

    def get_object(self):
        self.article = get_object_or_404(Article, slug=self.kwargs['slug'])

        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        return {
            "message": self.get_message(self.object),
            "object": self.object,
        }


@view_decorator(login_required)
class ArticleDeleteCommentView(RelatedArticleObjectMixin, DeleteView):
    model = ArticleComment
    template_name = "blog/confirm_change_article_object.dj.htm"

    def get_message(self, object):
        return "Really delete this comment? ({})".format(object)


@view_decorator(login_required)
class BaseArticleCommenterView(RelatedArticleObjectMixin, UpdateView):
    model = Commenter
    template_name = "blog/confirm_change_article_object.dj.htm"
    fields = ()

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class ArticleBanCommenterView(BaseArticleCommenterView):
    def get_message(self, object):
        return "Really ban this commenter? ({})".format(object)

    def form_valid(self, form):
        self.object.time_banned = timezone.now()
        self.object.save(update_fields=["time_banned"])

        return super().form_valid(form)


class ArticleUnbanCommenterView(BaseArticleCommenterView):
    def get_message(self, object):
        return "Really unban this commenter? ({})".format(object)

    def form_valid(self, form):
        self.object.time_banned = None
        self.object.save(update_fields=["time_banned"])

        return super().form_valid(form)


class ArticleMonthArchiveView (
    ArticleListMixin, MonthArchiveView, NavigationMixin
):
    date_field = "creation_date"
    make_object_list = True
    template_name = "blog/date.dj.htm"


class ArticleEditMixin:
    model = Article
    form_class = EditArticleForm
    template_name = "blog/post_edit.dj.htm"

    def get_success_url(self):
        return self.object.edit_url()


@view_decorator(login_required, transaction.atomic)
class EditArticleView(ArticleEditMixin, UpdateView):
    pass


@view_decorator(login_required, transaction.atomic)
class NewArticleView(ArticleEditMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


@login_required
def upload_file_view(request):
    """
    This view manages uploading a file to a site.
    """
    form = UploadForm(request.POST or None)

    if form.is_valid():
        upload = form.save(commit=False)
        upload.author = request.user
        upload.save()

        return JsonResponse(upload, safe=True, status_code=201)

    return JsonResponse(None, status_code=400)


class DeleteArticleView(DeleteView):
    model = Article
    context_object_name = "article"
    template_name = "blog/article_delete.dj.htm"
    success_url = reverse_lazy("article-edit-list", kwargs={"page": 1})


def bounce_view(request, url):
    return render(request, "blog/bounce.dj.htm", {
        "url": url() if callable(url) else url,
    })


def article_bounce_view(request, slug):
    return bounce_view(request, url_reverse(
        "article-detail",
        kwargs={"slug": slug},
    ) + "#last_comment")
