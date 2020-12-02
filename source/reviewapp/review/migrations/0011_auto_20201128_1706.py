# Generated by Django 3.1.3 on 2020-11-28 11:06

from django.db import migrations, models
import reviewapp.review.models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0010_item_descriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsfiles',
            name='media',
            field=models.FileField(upload_to=reviewapp.review.models.upload_image_path),
        ),
    ]
