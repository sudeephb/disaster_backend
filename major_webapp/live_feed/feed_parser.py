import feedparser as fp
import datetime
import pytz

def parser(url):
    return fp.parse(url)

def get_source(parsed):
    feed = parsed["feed"]
    return{
        "title" : feed["title"],
        "subtitle" : feed["subtitle"],
        "link" : feed["link"]
    }

def get_article(parsed):
    articles = []
    entries = parsed["entries"]
    for entry in entries:
        articles.append({
            "guid"  : entry["id"],
            "title" : entry["title"],
            "link"  : entry["link"],
            "published_date" : (datetime.datetime(*entry["published_parsed"][:6]) - datetime.timedelta(hours=5,minutes=45))
                                .replace(tzinfo=pytz.utc),
            "summary"   :   entry["summary"],
            "tags"  :   ",".join(list(map(lambda x:x.term,entry["tags"])))
        })
    return articles
