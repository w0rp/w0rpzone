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

from w0rplib.templatetags.markdown import unsafe_markdown

from . import models
from . import forms
from . import query

class NavigationMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "article_months" : query.all_article_months(),
        })

        return context

class ArticleListMixin:
    queryset = (
        models.Article.objects.all()
        .filter(active= True)
        .defer("content")
    )

    context_object_name = "article_list"

class ArticlePageView (ArticleListMixin, ListView, NavigationMixin):
    template_name = "blog/page.dj.htm"
    paginate_by = 10

class ArticleDetailView (DetailView, NavigationMixin):
    model = models.Article
    context_object_name = "article"
    template_name = "blog/detail.dj.htm"

    def get_queryset(self):
        return super().get_queryset().filter(active= True)

class ArticleMonthArchiveView (ArticleListMixin, MonthArchiveView,
NavigationMixin):
    date_field = "creation_date"
    make_object_list= True
    template_name = "blog/date.dj.htm"

@login_required
@transaction.atomic
def edit_article_view(request, slug):
    article = get_object_or_404(models.Article, slug=slug)

    form = forms.ArticleForm(request.POST or None, instance=article)
    updated = False

    if request.method == "POST" and form.is_valid():
        form.save()
        updated = True

        # When an edit works, reload the form to get the values
        # as they are set.
        form = forms.ArticleForm(instance= article)

    return render(request, "blog/post_edit.dj.htm", {
        "form": form,
        "updated": updated,
    })

@login_required
@transaction.atomic
def new_article_view(request):
    form = forms.ArticleForm(request.POST or None)

    if not form.is_valid():
        return render(request, "blog/post_edit.dj.htm", {
            "form" : form
        })

    article = form.save(author= request.user)

    return redirect(url_reverse(edit_article_view, args=[article.slug]))

@login_required
@csrf_exempt
def preview_markdown_view(request):
    text = request.POST.get("text")

    if text is None:
        return HttpResponse("No text supplied!", status=400)

    return HttpResponse(unsafe_markdown(text))

