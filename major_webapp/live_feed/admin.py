from django.contrib import admin
from .models import Source, Article, Log

# Register your models here.
admin.site.register(Source)
admin.site.register(Article)
admin.site.register(Log)
