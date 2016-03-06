from django.test import TestCase
from django.core.urlresolvers import reverse as url_reverse

from blog.feed import LatestArticleFeed
from blog.models import Article

from .util import (
    make_time,
    create_author,
    create_article,
    create_sample_article_list,
)


class ArticleTestCase(TestCase):
    def test_view_article(self):
        article = create_article(create_author())

        response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        self.assertIn('article', response.context)
        self.assertEqual(response.context['article'], article)
        self.assertContains(
            response,
            "<p><strong>Here</strong> is <em>some text</em></p>"
        )

    def test_front_page_shows_with_no_articles(self):
        self.assertEqual(self.client.get("/", follow=True).status_code, 200)


class ArticleFeedTestCase(TestCase):
    def test_feed_items(self):
        create_sample_article_list(create_author())

        self.assertEqual(
            [x.slug for x in LatestArticleFeed().items()],
            [
                "twelfth-article",
                "tenth-article",
                "ninth-article",
                "eigth-article",
                "seventh-article",
                "sixth-article",
                "fifth-article",
                "fourth-article",
                "third-article",
                "second-article",
                "first-article",
            ]
        )

    def test_feed_item_title(self):
        author = create_author(save=False)
        article = create_article(author, save=False)

        self.assertEqual(
            LatestArticleFeed().item_title(article),
            "Some Article",
        )

    def test_feed_item_description(self):
        author = create_author(save=False)
        article = create_article(author, save=False)

        self.assertEqual(
            LatestArticleFeed().item_description(article),
            "",
        )


class ArchiveTestCase(TestCase):
    def test_article_months_output(self):
        create_sample_article_list(create_author())

        self.assertEqual(
            list(Article.objects.active_months()),
            [
                make_time(2015, 6, 1),
                make_time(2014, 7, 1),
                make_time(2014, 6, 1),
            ],
            msg="The article months didn't match up!"
        )

    def test_view_month_article(self):
        create_sample_article_list(create_author())

        response = self.client.get(
            url_reverse("article-archive", kwargs={
                "year": "2014",
                "month": "06",
            }),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("article_list" in response.context)

        self.assertEqual(
            [x.slug for x in response.context["article_list"]],
            ["second-article", "first-article"]
        )

    def test_view_month_article_404(self):
        create_sample_article_list(create_author())

        response = self.client.get(
            url_reverse("article-archive", kwargs={
                "year": "2016",
                "month": "01",
            }),
        )

        self.assertEqual(response.status_code, 404)

    def test_front_page(self):
        create_sample_article_list(create_author())

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("article_list" in response.context)

        self.assertEqual(
            [x.slug for x in response.context["article_list"]],
            [
                "twelfth-article",
                "tenth-article",
                "ninth-article",
                "eigth-article",
                "seventh-article",
                "sixth-article",
                "fifth-article",
                "fourth-article",
                "third-article",
                "second-article",
            ]
        )

    def test_second_page(self):
        create_sample_article_list(create_author())

        response = self.client.get(
            url_reverse("article-page", kwargs={"page": 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("article_list" in response.context)

        self.assertEqual(
            [x.slug for x in response.context["article_list"]],
            ["first-article"]
        )
