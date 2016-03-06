from django.test import TestCase

from blog.models import ArticleTag

from .util import (
    create_author,
    create_article,
)


class ArticleModelTestCase(TestCase):
    def test_article_string(self):
        article = create_article(create_author(save=False), save=False)

        self.assertEqual(str(article), article.slug)

    def test_article_tag_string(self):
        article = create_article(create_author(save=False), save=False)

        tag = ArticleTag(article=article, tag="some-tag")

        self.assertEqual(str(tag), "{} - {}".format(tag.tag, article.slug))

    def test_article_modified_time_changed(self):
        article = create_article(create_author())

        original_modified_date = article.modified_date

        article.save()

        self.assertGreater(article.modified_date, original_modified_date)

    def test_article_preserve_modified_time(self):
        article = create_article(create_author())

        original_modified_date = article.modified_date

        article.save(timestamp=False)

        self.assertEqual(article.modified_date, original_modified_date)
