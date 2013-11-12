from django.views.generic import ListView
from django.views.generic.detail import DetailView

from . import models

class ArticlePageView (ListView):
    model = models.Article
    context_object_name = "article_list"
    template_name = "blog/page.dj.htm"
    paginate_by = 3

class ArticleDetailView (DetailView):
    model = models.Article
    context_object_name = "article"
    template_name = "blog/article.dj.htm"

