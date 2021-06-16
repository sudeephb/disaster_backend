# Run with proper django context
# ./manage.py shell < add_sources_data.py
from live_feed.models import Source
#"http://www.english.ratopati.com/feed/" # TODO look into it
sources_link = ["https://www.thehimalayantimes.com/feed/",
                "https://english.onlinekhabar.com/feed",
                "https://www.nepalitimes.com/feed/",
                "https://english.nepalpress.com/feed/"]


for link in sources_link:
    Source.add_source(url=link)