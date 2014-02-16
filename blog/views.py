import datetime
from functools import partial

from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse as url_reverse
from django.db import transaction
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.utils import timezone

from w0rplib.templatetags.markdown import unsafe_markdown, markdown

from .models import (
    Article,
    ArticleComment,
    Commenter,
)

from .forms import (
    EditArticleForm,
    NewArticleForm,
    ArticleCommentForm,
)

class NavigationMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context.update({
            "article_months": Article.objects.active_months()
        })

        return context

class ArticleListMixin:
    queryset = (
        Article.objects.all()
        .filter(active= True)
        .defer("content")
        .select_related("author")
    )

    context_object_name = "article_list"

class ArticlePageView (ArticleListMixin, ListView, NavigationMixin):
    template_name = "blog/page.dj.htm"
    paginate_by = 10

class ArticleEditPageView(ListView):
    queryset = (
        Article.objects.all()
        .defer("content")
    )

    context_object_name = "article_list"
    template_name = "blog/article_edit_list.dj.htm"
    paginate_by = 20

HONEYPOT_STRING = str(347 * 347)

def honeypot_ok(request, missing_name):
    return (
        not request.POST.get(missing_name)
        and request.POST.get("verify") == HONEYPOT_STRING
    )

def comment_on_article(article, request):
    """
    Given an article and a request object, process the request and add an
    article comment if needed and possible.
    """
    assert isinstance(article, Article)

    if "comment" not in request.POST:
        return ArticleCommentForm()

    comment_form = ArticleCommentForm(request.POST)

    commenter = Commenter.objects.create_for_ip(request.META["REMOTE_ADDR"])

    if not honeypot_ok(request, "title"):
        comment_form.add_error("__all__", "You are probably a spammer.")
    elif commenter.is_banned:
        comment_form.add_error("__all__", "You have been banned from posting.")
    elif commenter.is_comment_too_soon(timezone.now()):
        comment_form.add_error("__all__", "You cannot comment again so soon.")

    if comment_form.is_valid():
        # Add this comment.
        comment = comment_form.save(commit= False)

        comment.commenter = commenter
        comment.article = article
        comment.save()

    return comment_form

def article_or_404(slug):
    try:
        return (
            Article.objects
            .get(slug= slug)
        )
    except Article.DoesNotExist:
        return Http404

def article_detail_view(request, slug):
    article = article_or_404(slug)

    comment_form = comment_on_article(article, request)

    if comment_form.is_valid():
        # Redirect away to make it hard to accidentally submit twice.
        return redirect(url_reverse(
            "article-comment-bounce",
            args=[article.slug],
        ))

    return render(request, "blog/detail.dj.htm", {
        "article": article,
        "article_months": Article.objects.active_months(),
        "comment_default_name": ArticleComment.DEFAULT_NAME,
        "comment_form": comment_form,
    })

@login_required
def change_article_object_view(request, slug, pk, model, action, message):
    """
    A generic view for changing an object related somehow to an article.

    An instance of the given model will be retrieved with the given 'pk',
    and the action function will be called with the instance to perform
    the action, supposing the request is a post request and contains
    the key "apply_action", a confirmation page will be generated otherwise.
    """
    article = article_or_404(slug)

    try:
        obj = model.objects.get(pk= pk)
    except model.DoesNotExist:
        raise Http404

    if "apply_action" in request.POST:
        action(obj)

        return redirect(url_reverse(article_detail_view, args=[slug]))

    return render(request, "blog/confirm_change_article_object.dj.htm", {
        "message": message % obj,
        "object": obj,
    })

article_delete_comment_view = partial(
    change_article_object_view,
    model= ArticleComment,
    action= lambda obj: obj.delete(),
    message= "Really delete this comment? (%s)",
)

def ban_commenter(commenter):
    if commenter.time_banned is None:
        commenter.time_banned = timezone.now()
        commenter.save()

article_ban_commenter_view = partial(
    change_article_object_view,
    model= Commenter,
    action= ban_commenter,
    message= "Really ban this commenter? (%s)",
)

def unban_commenter(commenter):
    if commenter.time_banned is not None:
        commenter.time_banned = None
        commenter.save()

article_unban_commenter_view = partial(
    change_article_object_view,
    model= Commenter,
    action= unban_commenter,
    message= "Really unban this commenter? (%s)",
)

class ArticleMonthArchiveView (ArticleListMixin, MonthArchiveView,
NavigationMixin):
    date_field = "creation_date"
    make_object_list= True
    template_name = "blog/date.dj.htm"

@login_required
@transaction.atomic
def edit_article_view(request, slug):
    article = get_object_or_404(Article, slug=slug)

    form = EditArticleForm(request.POST or None, instance=article)
    updated = False

    if request.method == "POST" and form.is_valid():
        form.save()
        updated = True

        # When an edit works, reload the form to get the values
        # as they are set.
        form = EditArticleForm(instance= article)

    return render(request, "blog/post_edit.dj.htm", {
        "article": article,
        "form": form,
        "updated": updated,
    })

@login_required
@transaction.atomic
def new_article_view(request):
    form = NewArticleForm(request.POST or None)

    if not form.is_valid():
        return render(request, "blog/post_edit.dj.htm", {
            "form" : form
        })

    article = form.save(author= request.user)

    return redirect(url_reverse(edit_article_view, args=[article.slug]))

class DeleteArticleView(DeleteView):
    model = Article
    context_object_name = "article"
    template_name = "blog/article_delete.dj.htm"
    success_url = reverse_lazy(
        "article-edit-list",
        kwargs={
            "page": 1,
        }
    )

@login_required
@csrf_exempt
def preview_markdown_view(request):
    text = request.POST.get("text")

    if text is None:
        return HttpResponse("No text supplied!", status=400)

    return HttpResponse(unsafe_markdown(text))

@csrf_exempt
def preview_safe_markdown_view(request):
    text = request.POST.get("text")

    if text is None:
        return HttpResponse("No text supplied!", status=400)

    return HttpResponse(markdown(text))

def bounce_view(request, url):
    return render(request, "blog/bounce.dj.htm", {
        "url": url() if callable(url) else url,
    })

def article_bounce_view(request, slug):
    return bounce_view(request, url_reverse(
        article_detail_view,
        kwargs= {"slug": slug},
    ) + "#last_comment")
