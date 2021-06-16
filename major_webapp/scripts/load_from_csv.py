#run this by 'python3 manage.py runscript load_from_csv

import csv

from majorApp.models import News

def run():
    fhand = open('data/test_data.csv')
    reader = csv.reader(fhand)

    News.objects.all().delete()

    for row in reader:
        print(row)

        # news, created = News.objects.get_or_create(title_text = row[0],url = row[1], time = row[2], label = row[6])
        # news.save()

        news = News(title_text = row[0],url = row[1], time = row[2], label = row[6])
        news.save()