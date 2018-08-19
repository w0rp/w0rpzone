from django.test import TestCase
from django.urls import reverse as url_reverse

from blog.models import Article

from .util import create_article, create_author


class ArticleEditTestCase(TestCase):
    def test_add_new_article(self):
        author = create_author()

        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(
            url_reverse("new-article"),
            {
                "title": "Some Article",
                "slug": "some-article",
                "active": True,
                "content": "*Some* Article",
                "creation_date": "2015-06-01 00:00",
            }
        )

        edit_url = url_reverse("edit-article", kwargs={"slug": "some-article"})

        self.assertRedirects(response, edit_url)

        article = Article.objects.get(slug="some-article")

        self.assertEqual(article.title, "Some Article")
        self.assertEqual(article.slug, "some-article")
        self.assertTrue(article.active)
        self.assertEqual(article.content, "*Some* Article")

    def test_add_new_article_forbidden(self):
        response = self.client.post(
            url_reverse("new-article"),
            {
                "title": "Some Article",
                "slug": "some-article",
                "active": True,
                "content": "*Some* Article",
                "creation_date": "2015-06-01 00:00",
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertEqual(Article.objects.all().count(), 0)

    def test_edit_article(self):
        author = create_author()
        article = create_article(author)

        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(
            article.edit_url(),
            {
                "title": "New Title",
                "slug": "something-else",
                "active": True,
                "content": "Bla *Bla*",
                "creation_date": (
                    article.creation_date.strftime("%Y-%m-%d %H:%M")
                ),
            }
        )

        article.refresh_from_db()

        self.assertRedirects(response, article.edit_url())

        self.assertEqual(article.title, "New Title")
        self.assertEqual(article.slug, "something-else")
        self.assertTrue(article.active)
        self.assertEqual(article.content, "Bla *Bla*")

    def test_edit_article_forbidden(self):
        author = create_author()
        article = create_article(author)

        original_modified_date = article.modified_date

        response = self.client.post(
            article.edit_url(),
            {
                "title": "New Title",
                "slug": "something-else",
                "active": True,
                "content": "Bla *Bla*",
                "creation_date": (
                    article.creation_date.strftime("%Y-%m-%d %H:%M")
                ),
            }
        )

        self.assertEqual(response.status_code, 302)

        article.refresh_from_db()

        # Test that the article has not been modified.
        self.assertEqual(article.modified_date, original_modified_date)

    def test_delete_article(self):
        author = create_author()
        article = create_article(author)

        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(article.delete_url())

        self.assertRedirects(
            response,
            url_reverse("article-edit-list", kwargs={"page": 1})
        )

        self.assertEqual(Article.objects.all().count(), 0)
