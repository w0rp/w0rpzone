# Generated by Django 2.2.1 on 2019-05-12 00:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_remove_ip_addresses'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Upload',
        ),
    ]
