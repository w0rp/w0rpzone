from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, include, url

from w0rplib.url import redir

from .views import (
    ArticlePageView,
    ArticleEditPageView,
    article_detail_view,
    ArticleMonthArchiveView,
    edit_article_view,
    new_article_view,
    article_delete_comment_view,
    article_ban_commenter_view,
    article_unban_commenter_view,
    DeleteArticleView,
    preview_markdown_view,
)

from .feed import LatestArticleFeed

urlpatterns = patterns("blog.views",
    # Loading the main site gets you page 1.
    url(r"^$", ArticlePageView.as_view(), {"page": "1"},
        name= "blog-home",
    ),
    # Redirect the first page back to the blog main page, for SEO.
    redir(r"^page/0*1/$", "/blog"),
    # Redirect appending "login" to the blog URL to the right login URL,
    # which will redirect back to the blog.
    redir(r"^login/$", "/login/?next=/blog"),
    url(
        r"^page/(?P<page>[\d]+)/$",
        ArticlePageView.as_view(),
        name= "article-page"
    ),
    url(
        r"^delete/(?P<slug>[\w-]+)/$",
        login_required(DeleteArticleView.as_view()),
        name= "delete-article"
    ),
    url(
        r"^edit-page/(?P<page>[\d]+)/$",
        login_required(ArticleEditPageView.as_view()),
        name= "article-edit-list"
    ),
    url(
        r"^post/(?P<slug>[\w-]+)/$",
        article_detail_view,
        name= "article-detail"
    ),
    url(
        r"^post/(?P<slug>[\w-]+)/delete-comment/(?P<pk>\d+)/$",
        article_delete_comment_view,
        name= "delete-comment"
    ),
    url(
        r"^post/(?P<slug>[\w-]+)/ban-comment/(?P<pk>\d+)/$",
        article_ban_commenter_view,
        name= "ban-comment"
    ),
    url(
        r"^post/(?P<slug>[\w-]+)/unban-comment/(?P<pk>\d+)/$",
        article_unban_commenter_view,
        name= "unban-comment"
    ),
    url(
        r"^date/(?P<year>\d{4})/(?P<month>1[0-2]|0[1-9])/$",
        ArticleMonthArchiveView.as_view(month_format="%m"),
        name= "article-archive"
    ),
    url(
        r"^latest/feed/$",
        LatestArticleFeed(),
        name= "article-feed"
    ),
    url(r"^new/$", new_article_view),
    url(
        r"^edit/(?P<slug>[\w-]+)/$",
        edit_article_view,
        name= "edit-article"
    ),
    url(r"^preview_markdown/$", preview_markdown_view),
)

