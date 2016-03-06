import datetime

import pytz

from django.contrib.auth.models import User

from blog.models import (
    Article,
    ArticleComment,
    Commenter,
)


def make_time(*args):
    return datetime.datetime(*args, tzinfo=pytz.utc)


def create_author(save=True):
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

    if save:
        author.save()

    return author


def create_article(author, save=True):
    article = Article(
        author=author,
        title="Some Article",
        slug="some-article",
        active=True,
        content="**Here** is *some text*",
        creation_date=make_time(2015, 6, 1, 3, 4, 7),
        modified_date=make_time(2015, 6, 1, 3, 4, 7),
    )

    if save:
        article.save()

    return article


def create_comment(article, save=True):
    ip1 = Commenter(ip_address="10.1.1.1")

    if save:
        ip1.save()

    comment = ArticleComment(
        article=article,
        commenter=ip1,
        poster_name="Dave",
        content="**Some** text by *Dave*",
        creation_date=make_time(2015, 6, 1, 4),
        modified_date=make_time(2015, 6, 1, 4),
    )

    if save:
        comment.save()

    return comment


def create_sample_article_list(author):
    Article.objects.bulk_create([
        Article(
            author=author,
            title="First Article",
            slug="first-article",
            active=True,
            content="*First* Text",
            creation_date=make_time(2014, 6, 1, 13),
            modified_date=make_time(2014, 6, 1),
        ),
        Article(
            author=author,
            title="Second Article",
            slug="second-article",
            active=True,
            content="*Second* Text",
            creation_date=make_time(2014, 6, 1, 14),
            modified_date=make_time(2014, 6, 1),
        ),
        Article(
            author=author,
            title="Third Article",
            slug="third-article",
            active=True,
            content="*Third* Text",
            creation_date=make_time(2014, 7, 1),
            modified_date=make_time(2014, 7, 1),
        ),
        Article(
            author=author,
            title="Fourth Article",
            slug="fourth-article",
            active=True,
            content="*Fourth* Text",
            creation_date=make_time(2015, 6, 1),
            modified_date=make_time(2015, 6, 1),
        ),
        Article(
            author=author,
            title="Fifth Article",
            slug="fifth-article",
            active=True,
            content="*Fifth* Text",
            creation_date=make_time(2015, 6, 2),
            modified_date=make_time(2015, 6, 2),
        ),
        Article(
            author=author,
            title="Sixth Article",
            slug="sixth-article",
            active=True,
            content="*Sixth* Text",
            creation_date=make_time(2015, 6, 3),
            modified_date=make_time(2015, 6, 3),
        ),
        Article(
            author=author,
            title="Seventh Article",
            slug="seventh-article",
            active=True,
            content="*Seventh* Text",
            creation_date=make_time(2015, 6, 4),
            modified_date=make_time(2015, 6, 4),
        ),
        Article(
            author=author,
            title="Eigth Article",
            slug="eigth-article",
            active=True,
            content="*Eigth* Text",
            creation_date=make_time(2015, 6, 5),
            modified_date=make_time(2015, 6, 5),
        ),
        Article(
            author=author,
            title="Ninth Article",
            slug="ninth-article",
            active=True,
            content="*Ninth* Text",
            creation_date=make_time(2015, 6, 6),
            modified_date=make_time(2015, 6, 6),
        ),
        Article(
            author=author,
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
            author=author,
            title="Eleventh Article",
            slug="eleventh-article",
            active=False,
            content="*Eleventh* Text",
            creation_date=make_time(2015, 6, 8),
            modified_date=make_time(2015, 6, 8),
        ),
        Article(
            author=author,
            title="Twelfth Article",
            slug="twelfth-article",
            active=True,
            content="*Twelfth* Text",
            creation_date=make_time(2015, 6, 9),
            modified_date=make_time(2015, 6, 9),
        ),
    ])
