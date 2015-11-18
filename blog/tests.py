import datetime

import pytz

from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse as url_reverse
from django.contrib.auth.models import User
from django.conf import settings

from blog.models import (
    Article,
    ArticleComment,
    Commenter,
)


def create_author():
    author = User(
        username="test_user",
        first_name="Test",
        last_name="User",
        email="test@test.com",
        is_staff=True,
        is_active=True,
        is_superuser=True,
        last_login=make_time(2015, 6, 1),
        date_joined=make_time(2015, 6, 1),
    )
    author.set_password("lolwat")

    author.save()

    return author


def make_time(*args):
    return datetime.datetime(*args, tzinfo=pytz.utc)


class ArticleEditTest(TestCase):
    def test_add_new_article(self):
        pass

    def test_edit_article(self):
        pass

    def test_delete_article(self):
        pass


class ArticleTestCase(TestCase):
    def setUp(self):
        self.author = create_author()

    def create_article(self):
        article = Article(
            author=self.author,
            title="Some Article",
            slug="some-article",
            active=True,
            content="**Here** is *some text*",
            creation_date=make_time(2015, 6, 1, 3, 4, 7),
            modified_date=make_time(2015, 6, 1, 3, 4, 7),
        )

        article.save()

        return article

    def test_view_article(self):
        article = self.create_article()

        response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        self.assertIn('article', response.context)
        self.assertEqual(response.context['article'], article)
        self.assertContains(
            response,
            "<p><strong>Here</strong> is <em>some text</em></p>"
        )

    def test_view_comments(self):
        article = self.create_article()

        ip1 = Commenter(ip_address="10.1.1.1")
        ip1.save()
        ip2 = Commenter(ip_address="10.1.1.2")
        ip2.save()
        ip3 = Commenter(ip_address="10.1.1.3")
        ip3.save()

        ArticleComment.objects.bulk_create([
            ArticleComment(
                article=article,
                commenter=ip1,
                poster_name="Dave",
                content="**Some** text by *Dave*",
                creation_date=make_time(2015, 6, 1, 4),
                modified_date=make_time(2015, 6, 1, 4),
            ),
            ArticleComment(
                article=article,
                commenter=ip2,
                poster_name="Jane",
                content="**Some** text by *Jane*",
                creation_date=make_time(2015, 6, 1, 4, 1),
                modified_date=make_time(2015, 6, 1, 4, 1),
            ),
            ArticleComment(
                article=article,
                commenter=ip3,
                poster_name="Bob",
                content="**Some** text by *Bob*",
                creation_date=make_time(2015, 6, 1, 4, 2),
                modified_date=make_time(2015, 6, 1, 4, 2),
            ),
        ])

        response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        self.assertIn("article", response.context)

        comments = response.context["article"].comments.all()

        self.assertEqual(
            [x.poster_name for x in comments],
            ["Dave", "Jane", "Bob"]
        )

        self.assertContains(
            response,
            "<p><strong>Some</strong> text by <em>Dave</em></p>",
        )
        self.assertContains(
            response,
            "<p><strong>Some</strong> text by <em>Jane</em></p>",
        )
        self.assertContains(
            response,
            "<p><strong>Some</strong> text by <em>Bob</em></p>",
        )

    def test_add_comment(self):
        article = self.create_article()

        comment_response = self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
            "verify": str(347 * 347),
        }, follow=True)

        self.assertEqual(comment_response.status_code, 200)
        self.assertContains(
            comment_response,
            "url={}".format(article.get_absolute_url())
        )

        response = self.client.get(article.get_absolute_url())

        self.assertIn("article", response.context)

        comments = response.context["article"].comments.all()

        self.assertEqual([x.poster_name for x in comments], ["Bob"])
        self.assertContains(
            response,
            "<p><strong>New</strong> text</p>",
        )

    def test_email_sent_for_new_comment(self):
        article = self.create_article()

        comment_response = self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
            "verify": str(347 * 347),
        })

        self.assertEqual(comment_response.status_code, 302)

        comment = article.comments.all().get()

        self.assertEqual(len(mail.outbox), 1)

        comment_email = mail.outbox[0]

        self.assertEqual(comment_email.subject, "w0rp.com: New Comment")

        self.assertEqual(
            comment_email.body,
            "\n".join((
                "A new comment has been posted.",
                "",
                "Article: {}".format(article.title),
                "Link: {}{}".format(
                    settings.EXTERNAL_SITE_URL,
                    comment.get_absolute_url()
                ),
                "Name: Bob".format(comment.poster_name_or_default),
                "",
                "-" * 79,
                "",
                comment.content
            ))
        )

    def remove_comment(self):
        pass

    def test_ban_commenter(self):
        pass

    def test_front_page_shows_with_no_articles(self):
        self.assertEqual(self.client.get("/", follow=True).status_code, 200)


class ArchiveTestCase(TestCase):
    def setUp(self):
        self.author = create_author()

        Article.objects.bulk_create([
            Article(
                author=self.author,
                title="First Article",
                slug="first-article",
                active=True,
                content="*First* Text",
                creation_date=make_time(2014, 6, 1, 13),
                modified_date=make_time(2014, 6, 1),
            ),
            Article(
                author=self.author,
                title="Second Article",
                slug="second-article",
                active=True,
                content="*Second* Text",
                creation_date=make_time(2014, 6, 1, 14),
                modified_date=make_time(2014, 6, 1),
            ),
            Article(
                author=self.author,
                title="Third Article",
                slug="third-article",
                active=True,
                content="*Third* Text",
                creation_date=make_time(2014, 7, 1),
                modified_date=make_time(2014, 7, 1),
            ),
            Article(
                author=self.author,
                title="Fourth Article",
                slug="fourth-article",
                active=True,
                content="*Fourth* Text",
                creation_date=make_time(2015, 6, 1),
                modified_date=make_time(2015, 6, 1),
            ),
            Article(
                author=self.author,
                title="Fifth Article",
                slug="fifth-article",
                active=True,
                content="*Fifth* Text",
                creation_date=make_time(2015, 6, 2),
                modified_date=make_time(2015, 6, 2),
            ),
            Article(
                author=self.author,
                title="Sixth Article",
                slug="sixth-article",
                active=True,
                content="*Sixth* Text",
                creation_date=make_time(2015, 6, 3),
                modified_date=make_time(2015, 6, 3),
            ),
            Article(
                author=self.author,
                title="Seventh Article",
                slug="seventh-article",
                active=True,
                content="*Seventh* Text",
                creation_date=make_time(2015, 6, 4),
                modified_date=make_time(2015, 6, 4),
            ),
            Article(
                author=self.author,
                title="Eigth Article",
                slug="eigth-article",
                active=True,
                content="*Eigth* Text",
                creation_date=make_time(2015, 6, 5),
                modified_date=make_time(2015, 6, 5),
            ),
            Article(
                author=self.author,
                title="Ninth Article",
                slug="ninth-article",
                active=True,
                content="*Ninth* Text",
                creation_date=make_time(2015, 6, 6),
                modified_date=make_time(2015, 6, 6),
            ),
            Article(
                author=self.author,
                title="Tenth Article",
                slug="tenth-article",
                active=True,
                content="*Tenth* Text",
                creation_date=make_time(2015, 6, 7),
                modified_date=make_time(2015, 6, 7),
            ),
            # This article will not be active,
            # so we should ignore it in the list.
            Article(
                author=self.author,
                title="Eleventh Article",
                slug="eleventh-article",
                active=False,
                content="*Eleventh* Text",
                creation_date=make_time(2015, 6, 8),
                modified_date=make_time(2015, 6, 8),
            ),
            Article(
                author=self.author,
                title="Twelfth Article",
                slug="twelfth-article",
                active=True,
                content="*Twelfth* Text",
                creation_date=make_time(2015, 6, 9),
                modified_date=make_time(2015, 6, 9),
            ),
        ])

    def test_article_months_output(self):
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
        response = self.client.get(
            url_reverse("article-archive", kwargs={
                "year": "2016",
                "month": "01",
            }),
        )

        self.assertEqual(response.status_code, 404)

    def test_front_page(self):
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
        response = self.client.get(
            url_reverse("article-page", kwargs={"page": 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("article_list" in response.context)

        self.assertEqual(
            [x.slug for x in response.context["article_list"]],
            ["first-article"]
        )
