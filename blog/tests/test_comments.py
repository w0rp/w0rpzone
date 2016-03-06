from django.test import TestCase
from django.core import mail
from django.conf import settings

from blog.models import (
    ArticleComment,
    Commenter,
)

from .util import (
    make_time,
    create_article,
    create_author,
    create_comment,
)


class ArticleCommentTestCase(TestCase):
    def test_view_comments(self):
        article = create_article(create_author())

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
        article = create_article(create_author())

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

    def test_add_comment_no_verify_string(self):
        article = create_article(create_author())

        comment_response = self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
        })

        self.assertEqual(comment_response.status_code, 200)

        # Nothing should have been submitted.
        self.assertEqual(ArticleComment.objects.all().count(), 0)

    def test_add_comment_rubbish_string(self):
        article = create_article(create_author())

        comment_response = self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
            "title": "anything",
        })

        self.assertEqual(comment_response.status_code, 200)

        # Nothing should have been submitted.
        self.assertEqual(ArticleComment.objects.all().count(), 0)

    def test_add_comment_too_soon(self):
        article = create_article(create_author())

        self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
            "verify": str(347 * 347),
        })

        comment_response = self.client.post(article.get_absolute_url(), {
            "comment": None,
            "poster_name": "Bob",
            "content": "**New** text",
            "verify": str(347 * 347),
        })

        # This form should be invalid.
        self.assertEqual(comment_response.status_code, 200)

        # One the first comment should have been submitted.
        self.assertEqual(ArticleComment.objects.all().count(), 1)

    def test_add_comment_while_banned(self):
        article = create_article(create_author())

        commenter = Commenter(
            ip_address="10.1.1.1",
            time_banned=make_time(2015, 6, 1)
        )
        commenter.save()

        comment_response = self.client.post(
            article.get_absolute_url(),
            {
                "comment": None,
                "poster_name": "Bob",
                "content": "**New** text",
                "verify": str(347 * 347),
            },
            REMOTE_ADDR=commenter.ip_address,
        )

        # This form should be invalid.
        self.assertEqual(comment_response.status_code, 200)

        # Nothing should have been submitted.
        self.assertEqual(ArticleComment.objects.all().count(), 0)

    def test_email_sent_for_new_comment(self):
        article = create_article(create_author())

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

    def test_load_delete_comment_view(self):
        author = create_author()
        article = create_article(author)

        self.client.login(username=author.username, password="lolwat")

        comment = create_comment(article)

        response = self.client.get(comment.delete_url())

        self.assertEqual(response.status_code, 200)

        self.assertIn("object", response.context)
        self.assertEqual(response.context["object"], comment)

        # Nothing should have been deleted.
        self.assertEqual(ArticleComment.objects.all().count(), 1)
