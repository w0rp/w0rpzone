from django.conf.urls import re_path
from django.contrib.auth.decorators import login_required

from w0rplib.url import redir

from .feed import LatestArticleFeed
from .views import (
    ArticleBanCommenterView,
    ArticleDeleteCommentView,
    ArticleDetailView,
    ArticleEditPageView,
    ArticleMonthArchiveView,
    ArticlePageView,
    ArticleUnbanCommenterView,
    DeleteArticleView,
    EditArticleView,
    NewArticleView,
    article_bounce_view,
    upload_file_view,
)

urlpatterns = [
    # Loading the main site gets you page 1.
    re_path(
        r"^$",
        ArticlePageView.as_view(),
        {"page": "1"},
        name="blog-home",
    ),
    # Redirect the first page back to the blog main page, for SEO.
    redir(r"^page/0*1/$", "/blog"),
    # Redirect appending "login" to the blog URL to the right login URL,
    # which will redirect back to the blog.
    redir(r"^login/$", "/login/?next=/blog"),
    re_path(
        r"^page/(?P<page>[\d]+)/$",
        ArticlePageView.as_view(),
        name="article-page"
    ),
    re_path(
        r"^delete/(?P<slug>[\w-]+)/$",
        login_required(DeleteArticleView.as_view()),
        name="delete-article"
    ),
    re_path(
        r"^edit-page/(?P<page>[\d]+)/$",
        login_required(ArticleEditPageView.as_view()),
        name="article-edit-list"
    ),
    re_path(
        r"^post/(?P<slug>[\w-]+)/$",
        ArticleDetailView.as_view(),
        name="article-detail"
    ),
    re_path(
        r"^post/(?P<slug>[\w-]+)/comment-bounce/$",
        article_bounce_view,
        name="article-comment-bounce"
    ),
    re_path(
        r"^post/(?P<slug>[\w-]+)/delete-comment/(?P<pk>\d+)/$",
        ArticleDeleteCommentView.as_view(),
        name="delete-comment"
    ),
    re_path(
        r"^post/(?P<slug>[\w-]+)/ban-comment/(?P<pk>\d+)/$",
        ArticleBanCommenterView.as_view(),
        name="ban-commenter"
    ),
    re_path(
        r"^post/(?P<slug>[\w-]+)/unban-comment/(?P<pk>\d+)/$",
        ArticleUnbanCommenterView.as_view(),
        name="unban-commenter"
    ),
    re_path(
        r"^date/(?P<year>\d{4})/(?P<month>1[0-2]|0[1-9])/$",
        ArticleMonthArchiveView.as_view(month_format="%m"),
        name="article-archive"
    ),
    re_path(
        r"^latest/feed/$",
        LatestArticleFeed(),
        name="article-feed"
    ),
    re_path(
        r"^new/$",
        NewArticleView.as_view(),
        name="new-article",
    ),
    re_path(
        r"^edit/(?P<slug>[\w-]+)/$",
        EditArticleView.as_view(),
        name="edit-article"
    ),
    re_path(r"^upload/$", upload_file_view, name="upload-file"),
]
