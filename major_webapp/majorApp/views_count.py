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





# @csrf_exempt
class disaster(APIView):
    def get(self, request):
        news_count = News.objects.all().count()
        return HttpResponse(json.dumps(news_count), content_type='application/json')


    def post(self, request):
        category = []
        if ("level" in request.data[0]):
            hierarchy_level = request.data[0]["level"]
            category = request.data[0]['category']
            if hierarchy_level == 'label2':
                if category == 'all':
                    news_count = News.objects.all().count()
                else:
                    news_count = News.objects.filter(label2=category).count()
            elif hierarchy_level == 'label3':
                news_count = News.objects.filter(label3=category).count()

            return HttpResponse(json.dumps(news_count), content_type='application/json')

        for x in request.data:
            if x["is_selected"] == "True" or x["is_selected"] == "true":
                category.append(x["label_name"])
        news_count = News.objects.filter(label__in=category).count()
        return HttpResponse(json.dumps(news_count), content_type='application/json')


