# Generated by Django 3.1.3 on 2020-11-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0005_auto_20201123_1610'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-created'], 'verbose_name': 'review', 'verbose_name_plural': 'reviews'},
        ),
        migrations.AddField(
            model_name='item',
            name='likes',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='review',
            name='likes',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
    ]
