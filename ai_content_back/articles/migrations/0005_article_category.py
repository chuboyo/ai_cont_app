# Generated by Django 4.1.1 on 2023-11-04 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_alter_article_options_article_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
