import requests

import xml.etree.ElementTree as ET


class RssFeed:

    def __init__(self, url):
        self.url = url
        self.news = []


    def fetch_news(self):
        response = requests.get(self.url)

        root = ET.fromstring(response.text)

        self.news.clear()
        for item in root[0].findall("item"):
            self.news.append(item.find("link").text)

        return self.news

if __name__ == "__main__":
    rssfeed = RssFeed('http://www.varzesh3.com/rss/all')
    print(rssfeed.fetch_news())
