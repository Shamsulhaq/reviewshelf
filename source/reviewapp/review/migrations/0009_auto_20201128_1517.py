# Generated by Django 3.1.3 on 2020-11-28 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_auto_20201128_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, null=True, unique=True),
        ),
    ]
