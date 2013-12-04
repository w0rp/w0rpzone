from django.conf.urls import patterns, include, url

from w0rplib.url import redir

from .views import (
    ArticlePageView,
    ArticleDetailView,
    ArticleMonthArchiveView,
    edit_article_view,
    new_article_view,
    preview_markdown_view,
)

from .feed import LatestArticleFeed

urlpatterns = patterns("blog.views",
    # Loading the main site gets you page 1.
    (r"^$", ArticlePageView.as_view(), {"page": "1"}),
    # Redirect the first page back to the blog main page, for SEO.
    redir(r"^page/0*1/$", "/blog"),
    url(
        r"^page/(?P<page>[\d]+)/$",
        ArticlePageView.as_view(),
        name= "article-page"
    ),
    url(
        r"^post/(?P<slug>[\w-]+)/$",
        ArticleDetailView.as_view(),
        name= "article-detail"
    ),
    url(
        r"^date/(?P<year>\d{4})/(?P<month>1[0-2]|0[1-9])/$",
        ArticleMonthArchiveView.as_view(month_format="%m"),
        name= "article-archive"
    ),
    (r"^latest/feed/$", LatestArticleFeed()),
    url(r"^new/$", new_article_view),
    url(r"^edit/(?P<slug>[\w-]+)/$", edit_article_view),
    url(r"^preview_markdown/$", preview_markdown_view),
)

