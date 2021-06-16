from django.http import HttpResponse
import json
from django.shortcuts import render
from .models import News
from .serializers import newsSerializer
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


NEWS_PER_PAGE = 15

def index(request):
    label_set = set()
    
    selected_disaster_type = ''

    if request.method == 'GET':
        selected_disaster_type = request.GET.get('selected_disaster_type', '')
        # print('*************')
        # print(request.GET.get('selected_disaster_type', ''))
        # print('*************')

    if selected_disaster_type:
        news_all = News.objects.filter(label = selected_disaster_type)
    else:
        news_all = News.objects.all()
    # news_all = News.objects.all()
    for news in News.objects.all():
        label_set.add(news.label)
    context = {
        'news_all': news_all,
        'label_set': label_set,
        'selected_disaster_type': selected_disaster_type
    }
    return render(request, 'home.html', context)


def selected_disaster(request, label):
    #label = selected_disaster (eg: earthquake)
    news_all = News.objects.filter(label=label)

    label_set = set()
    for news in News.objects.all():
        label_set.add(news.label)
        
    context = {
        'news_all': news_all,
        'label_set': label_set
    }
    return render(request, 'home.html', context)

def labels(APIView):
    # def get(self, request):
    label_set = set()

    for news in News.objects.all():
        label_set.add(news.label)


    return HttpResponse(json.dumps(list(label_set)), content_type='application/json')


# @csrf_exempt
class disaster(APIView):
    def get(self, request):
        page_no = request.GET.get('page_no', None)
        # print('====Get request without any post data======')
        news = News.objects.all().order_by('-time')
        if page_no is not None:
            print('Query param ==== ', page_no)
            page_no = int(page_no) - 1
            if NEWS_PER_PAGE*page_no+NEWS_PER_PAGE < news.count():
                news = news[NEWS_PER_PAGE*page_no:NEWS_PER_PAGE*page_no+NEWS_PER_PAGE]
            else:
                news = news[NEWS_PER_PAGE*page_no:]
            serializer = newsSerializer(news, many=True)
            return Response(serializer.data)
        news = news[:2]
        serializer = newsSerializer(news, many=True)
        return Response(serializer.data)

    #label2 = natural, technological
    #label3 = geophysical, meteorological.....
    # send as [{'level': 'label2'
    #             'category': 'natural'  }]
    def post(self, request):
        category = []
        page_no = request.GET.get('page_no', None)
        print('Request.data===== ', request.data)
        if ("level" in request.data[0]):
            # print('Request.data =========> ', request.data)
            hierarchy_level = request.data[0]["level"]
            category = request.data[0]['category']
            if hierarchy_level == 'label2':
                # print('Request.data =========> ', category)
                if category == 'all':
                    news = News.objects.all().order_by('-time')
                else:
                    news = News.objects.filter(label2=category).order_by('-time')
            elif hierarchy_level == 'label3':
                # print('Category ==== = = = =, ', category)
                news = News.objects.filter(label3=category).order_by('-time')
            
            if page_no is not None:
                print('Query param ==== ', page_no)
                page_no = int(page_no) - 1
                if NEWS_PER_PAGE*page_no+NEWS_PER_PAGE < news.count():
                    news = news[NEWS_PER_PAGE*page_no:NEWS_PER_PAGE*page_no+NEWS_PER_PAGE]
                else:
                    news = news[NEWS_PER_PAGE*page_no:]
                serializer = newsSerializer(news, many=True)
                return Response(serializer.data)


            news = news[:5]
            serializer = newsSerializer(news, many=True)
            return Response(serializer.data)

        print('== = = = = ', request.data)
        for x in request.data:
            if x["is_selected"] == "True" or x["is_selected"] == "true":
                category.append(x["label_name"])
        print('category = ', category)
        news = News.objects.filter(label__in=category).order_by('-time')


        if page_no is not None:
            print('Query param ==== ', page_no)
            page_no = int(page_no) - 1
            if NEWS_PER_PAGE*page_no+NEWS_PER_PAGE < news.count():
                news = news[NEWS_PER_PAGE*page_no:NEWS_PER_PAGE*page_no+NEWS_PER_PAGE]
            else:
                news = news[NEWS_PER_PAGE*page_no:]
            serializer = newsSerializer(news, many=True)
            return Response(serializer.data)


        news = news[:5]
        serializer = newsSerializer(news, many=True)
        return Response(serializer.data)


