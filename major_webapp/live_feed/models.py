from django.db import models
from django.utils import timezone
from live_feed.feed_parser import parser, get_article, get_source

# Create your models here.
class Source(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=False,max_length=200)
    subtitle = models.CharField(blank=False,max_length=200)
    link = models.CharField(blank=False,max_length=200)
    feedlink = models.CharField(blank=False,max_length=200,unique=True)
    date_added = models.DateTimeField(default=timezone.now)

    #For only standarized rss.
    @classmethod
    def add_source(*args,**kargs):
        url = kargs["url"]
        parsed = parser(url)
        source_info = get_source(parsed)
        Source.objects.create(
            title=source_info["title"],
            subtitle=source_info["subtitle"],
            link=source_info["link"],
            feedlink=url
        )

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.CharField(blank=False,max_length=200)
    title = models.CharField(blank=False,max_length=200)
    summary = models.TextField(blank=False)
    link = models.CharField(blank=False,max_length=200)
    tags = models.CharField(blank=False,max_length=500)
    published_date = models.DateTimeField()
    date_added = models.DateTimeField(default=timezone.now)
    classified = models.BooleanField(default=False)
    source = models.ForeignKey(Source,on_delete=models.PROTECT)
    class Meta:
        unique_together = ["guid", "source"]
    
    @classmethod
    def insert_articles_from_sources(cls):
        articles = []
        for source in Source.objects.all():
            parsed_feed = parser(source.feedlink)
            parsed_articles = get_article(parsed_feed)
            for parsed_article in parsed_articles:
                article = Article(
                        guid=parsed_article["guid"],
                        title=parsed_article["title"],
                        link=parsed_article["link"],
                        published_date=str(parsed_article["published_date"]),
                        summary=parsed_article["summary"],
                        tags=parsed_article["tags"],
                        source=source
                    )
                articles.append(article)
        Article.objects.bulk_create(articles,ignore_conflicts=True)
        return articles

class Log(models.Model):
    status = models.CharField(max_length=2,choices=[("S","Success"),("F","Failure")],blank=False)
    updated_at = models.DateTimeField(default=timezone.now)
        

