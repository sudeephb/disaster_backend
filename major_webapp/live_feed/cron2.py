from binary_classifier.binary_classifier import predict
from live_feed.models import Article
from majorApp.models import News
import requests
import json

ENDPOINT = "http://127.0.0.1:8000/hierarchical_classifier/"

def get_class(json_array):
    r = requests.post(url=ENDPOINT, json=json_array)
    return r

def classify_news():
    print("running")
    #classification
    articles = Article.objects.filter(classified=False).all()
    for article in articles:
        article.classified = True
        article.save()
        label1 = predict(article.title)
        if label1 == 'DISASTER_':
            news_json = [{"id":article.id, "title": article.title}]
            hierarchy_result = json.loads(get_class(news_json).text)[0] #Because we are only passing one json and get one response json back
            label2 = hierarchy_result["label1"]
            label3 = hierarchy_result["label2"]
            label = hierarchy_result["label3"]
            news = News(title_text = article.title, url = article.link, 
                        time = article.published_date, source=article.source,
                        summary = article.summary,
                        label1 = label1, label2=label2, label3=label3,label=label)
            print(news)
            news.save()
