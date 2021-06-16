from django.db import models
from live_feed.models import Source

# Create your models here.
class News(models.Model):
    title_text = models.TextField()
    url = models.URLField(null=True)
    time = models.DateTimeField()
    source = models.ForeignKey(Source,on_delete=models.PROTECT)
    summary = models.TextField(null=True)

    label = models.CharField(max_length = 30, null = True) #this is leaf_label
    label1 = models.CharField(max_length=30, null=True)
    label2 = models.CharField(max_length=30, null=True)
    label3 = models.CharField(max_length=30, null=True)




    class Meta:
        verbose_name_plural = "News"
        unique_together = ["title_text", "source"]

    def __str__(self):
        return self.title_text
    
