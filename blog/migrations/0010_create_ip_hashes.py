import hashlib
from django.db import migrations


def create_hashes_from_ip_addresses(apps, schema_editor):
    Commenter = apps.get_model('blog', 'Commenter')

    for commenter in Commenter.objects.all():
        commenter.ip_hash = (
            hashlib.sha256(commenter.ip_address.encode("utf-8"))
            .digest()
            .hex()
        )
        commenter.save(update_fields=['ip_hash'])

    Commenter.objects.filter(comments__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_add_ip_hash_field'),
    ]

    operations = [
        migrations.RunPython(
            create_hashes_from_ip_addresses,
            migrations.RunPython.noop,
        ),
    ]
