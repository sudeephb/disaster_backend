from rest_framework import serializers
from .models import News

class newsSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField()
    source_name = serializers.SerializerMethodField('get_source_name')
    source_link = serializers.SerializerMethodField('get_source_link')
    published_date_readable = serializers.SerializerMethodField('get_published_date_readable')
    class Meta:
        model = News
        fields = '__all__'
    
    def get_source_name(self,news):
        return news.source.title
    
    def get_source_link(self,news):
        return news.source.link
    
    def get_published_date_readable(self,news):
        return news.time.strftime('%b. %d, %Y, %I:%M %p')
