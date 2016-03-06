from django.test import TestCase

from blog.models import (
    ArticleComment,
    Commenter,
)

from .util import (
    make_time,
    create_author,
    create_article,
    create_comment,
)


class ArticleAdminControlsTestCase(TestCase):
    def test_delete_comment(self):
        author = create_author()
        article = create_article(author)

        self.client.login(username=author.username, password="lolwat")

        comment = create_comment(article)

        response = self.client.post(comment.delete_url())

        self.assertRedirects(response, article.get_absolute_url())

        self.assertEqual(ArticleComment.objects.all().count(), 0)

    def test_delete_comment_forbidden(self):
        article = create_article(create_author())

        comment = create_comment(article)

        response = self.client.post(comment.delete_url())

        self.assertEqual(response.status_code, 302)

        self.assertEqual(ArticleComment.objects.all().count(), 1)

    def test_load_ban_commenter_form(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(ip_address="10.1.1.1")
        commenter.save()

        self.client.login(username=author.username, password="lolwat")

        response = self.client.get(commenter.ban_url(article))

        self.assertEqual(response.status_code, 200)

    def test_ban_commenter(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(ip_address="10.1.1.1")
        commenter.save()

        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(commenter.ban_url(article))

        self.assertRedirects(response, article.get_absolute_url())

        commenter.refresh_from_db()

        # They should be flagged as being banned.
        self.assertIsNotNone(commenter.time_banned)

    def test_ban_commenter_forbidden(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(ip_address="10.1.1.1")
        commenter.save()

        response = self.client.post(commenter.ban_url(article))

        self.assertEqual(response.status_code, 302)

        commenter.refresh_from_db()

        # They should not have been banned.
        self.assertIsNone(commenter.time_banned)

    def test_load_unban_commenter_form(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(ip_address="10.1.1.1")
        commenter.save()

        self.client.login(username=author.username, password="lolwat")

        response = self.client.get(commenter.unban_url(article))

        self.assertEqual(response.status_code, 200)

    def test_unban_commenter(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(
            ip_address="10.1.1.1",
            time_banned=make_time(2015, 6, 1)
        )
        commenter.save()

        self.client.login(username=author.username, password="lolwat")

        response = self.client.post(commenter.unban_url(article))

        self.assertRedirects(response, article.get_absolute_url())

        commenter.refresh_from_db()

        # They should be unbanned now.
        self.assertIsNone(commenter.time_banned)

    def test_unban_commenter_forbidden(self):
        author = create_author()
        article = create_article(author)

        commenter = Commenter(
            ip_address="10.1.1.1",
            time_banned=make_time(2015, 6, 1)
        )
        commenter.save()

        response = self.client.post(commenter.unban_url(article))

        self.assertEqual(response.status_code, 302)

        commenter.refresh_from_db()

        # They should still be banned.
        self.assertIsNotNone(commenter.time_banned)
