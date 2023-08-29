# Generated by Django 4.1.1 on 2023-08-20 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField(blank=True)),
                ('source', models.CharField(blank=True, max_length=200)),
                ('paragraph_one', models.TextField(blank=True)),
                ('paragraph_two', models.TextField(blank=True)),
                ('read_count', models.IntegerField(blank=True)),
            ],
        ),
    ]