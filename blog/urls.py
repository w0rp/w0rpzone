from django.conf.urls import patterns, include, url

urlpatterns = patterns("blog.views",
    url(r"^$", "blog_main_page"),
    url(r"^post/(?P<article_slug>[\w-]+)/$", "blog_article_page"),
)

