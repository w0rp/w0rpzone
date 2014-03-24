from django.contrib.syndication.views import Feed

from . import models


class LatestArticleFeed(Feed):
    title = "w0rpzone Articles"
    link = "/blog/"

    def items(self):
        return (
            models.Article.objects
            .filter(active=True)
            .order_by("-creation_date")[:20]
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return ""
