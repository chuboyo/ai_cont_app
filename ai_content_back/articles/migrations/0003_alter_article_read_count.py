# Generated by Django 4.1.1 on 2023-08-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_read_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='read_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
