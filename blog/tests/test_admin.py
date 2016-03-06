from django.test import TestCase

from blog.models import (
    ArticleComment,
    Commenter,
)
from blog.admin import (
    CommenterAdmin,
    ArticleCommentAdmin,
)

from .util import (
    make_time,
    create_article,
    create_author,
    create_comment,
)


class AdminTestCase(TestCase):
    def test_ban_all(self):
        Commenter.objects.bulk_create([
            Commenter(ip_address="10.1.1.1"),
            Commenter(ip_address="10.1.1.2"),
            Commenter(ip_address="10.1.1.3"),
        ])

        queryset = Commenter.objects.filter(ip_address__in=[
            "10.1.1.1",
            "10.1.1.2",
        ])

        admin = CommenterAdmin(ArticleComment, None)

        admin.ban_all(None, queryset)

        self.assertEqual(
            list(
                Commenter.objects
                .filter(time_banned__isnull=True)
                .values_list("ip_address", flat=True)
            ),
            ["10.1.1.3"],
        )

    def test_unban_all(self):
        time_banned = make_time(2015, 6, 1)

        Commenter.objects.bulk_create([
            Commenter(ip_address="10.1.1.1", time_banned=time_banned),
            Commenter(ip_address="10.1.1.2", time_banned=time_banned),
            Commenter(ip_address="10.1.1.3", time_banned=time_banned),
        ])

        queryset = Commenter.objects.filter(ip_address__in=[
            "10.1.1.1",
            "10.1.1.2",
        ])

        admin = CommenterAdmin(ArticleComment, None)

        admin.unban_all(None, queryset)

        self.assertEqual(
            list(
                Commenter.objects
                .filter(time_banned__isnull=False)
                .values_list("ip_address", flat=True)
            ),
            ["10.1.1.3"],
        )

    def test_commenter_link_not_saved(self):
        article = create_article(create_author(save=False), save=False)

        comment = create_comment(article, save=False)

        self.assertEqual(
            ArticleCommentAdmin(ArticleComment, None).commenter_link(comment),
            "(None)"
        )

    def test_commenter_link(self):
        article = create_article(create_author(save=False), save=False)

        comment = create_comment(article, save=False)

        comment.commenter.pk = 1
        comment.pk = 1

        self.assertEqual(
            ArticleCommentAdmin(ArticleComment, None).commenter_link(comment),
            '<a href="/admin/blog/commenter/1/">10.1.1.1</a>'
        )
