from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse as url_reverse
from django.db import transaction

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

class ArticlePageView (ListView, NavigationMixin):
    queryset = models.Article.objects.all().defer("content")
    context_object_name = "article_list"
    template_name = "blog/page.dj.htm"
    paginate_by = 10

class ArticleDetailView (DetailView, NavigationMixin):
    model = models.Article
    context_object_name = "article"
    template_name = "blog/detail.dj.htm"

class ArticleMonthArchiveView (MonthArchiveView, NavigationMixin):
    queryset = models.Article.objects.all().defer("content")
    context_object_name = "article_list"
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

