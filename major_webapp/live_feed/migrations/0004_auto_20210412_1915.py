# Generated by Django 3.1.1 on 2021-04-12 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_feed', '0003_article_classified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.CharField(max_length=500),
        ),
    ]