from django.conf.urls import patterns, include, url

from w0rplib.url import redir

from blog.views import (
    ArticlePageView,
    ArticleDetailView,
)

urlpatterns = patterns("blog.views",
    # Loading the main site gets you page 1.
    (r"^$", ArticlePageView.as_view(), {"page": "1"}),
    # Redirect the first page back to the blog main page, for SEO.
    redir(r"^page/0*1/$", "/blog"),
    (r"^page/(?P<page>[\d]+)/$", ArticlePageView.as_view()),
    url(
        r"^post/(?P<slug>[\w-]+)/$",
        ArticleDetailView.as_view(),
        name= "article-detail"
    ),
)

