from live_feed.models import Article,Log
import datetime

def get_feed():
    try:
        articles = Article.insert_articles_from_sources()
        # Article.insert_articles_from_sources()
        Log.objects.create(status="S")
    except Exception:
        Log.objects.create(status="F")

