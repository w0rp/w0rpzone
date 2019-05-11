from django.db import migrations


def remove_commenters_without_post(apps, schema_editor):
    Commenter = apps.get_model('blog', 'Commenter')

    Commenter.objects.filter(comments__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_protect_articles_from_user_deletion'),
    ]

    operations = [
        migrations.RunPython(
            remove_commenters_without_post,
            migrations.RunPython.noop,
            elidable=True,
        ),
    ]
