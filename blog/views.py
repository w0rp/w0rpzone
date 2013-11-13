from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.dates import MonthArchiveView
from django.views.generic.detail import DetailView

from . import models
from . import query

class NavigationMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "article_months" : query.all_article_months(),
        })

        return context

class ArticlePageView (ListView, NavigationMixin):
    model = models.Article
    context_object_name = "article_list"
    template_name = "blog/page.dj.htm"
    paginate_by = 3

class ArticleDetailView (DetailView, NavigationMixin):
    model = models.Article
    context_object_name = "article"
    template_name = "blog/detail.dj.htm"

class ArticleMonthArchiveView (MonthArchiveView, NavigationMixin):
    queryset = models.Article.objects.all()
    context_object_name = "article_list"
    date_field = "creation_date"
    make_object_list= True
    template_name = "blog/date.dj.htm"

