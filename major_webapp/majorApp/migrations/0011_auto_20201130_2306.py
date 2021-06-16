# Generated by Django 3.1.1 on 2020-11-30 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('live_feed', '0003_article_classified'),
        ('majorApp', '0010_auto_20201129_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='source',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='live_feed.source'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='news',
            unique_together={('title_text', 'source')},
        ),
    ]
