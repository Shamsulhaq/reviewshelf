# Generated by Django 3.1.3 on 2020-11-28 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_category_is_deleted'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UnitOfHistory',
        ),
    ]
