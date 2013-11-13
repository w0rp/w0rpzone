from django.conf.urls import patterns, include, url

from w0rplib.url import redir

from blog.views import (
    ArticlePageView,
    ArticleDetailView,
    ArticleMonthArchiveView,
)

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
)

