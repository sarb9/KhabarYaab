import requests
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import heapq
import time
from collections import deque
from models import news_model
from datetime import datetime
from utils.import_utils import remove_tags

RSS_FEEDS = ["http://www.varzesh3.com/rss/foreignFootball",
             "http://www.varzesh3.com/rss/all",
             "http://www.varzesh3.com/rss/domesticFootball"]


class RssFeed:

    COOL_DOWN = 5

    def __init__(self, url):
        print(time.time())
        self.url = url
        self.point = -10000

        self.news = []
        self.seen_urls = set()
        self.back_queue = deque()

        self.last_visit = 0

    def update(self):
        if time.time() - self.last_visit < RssFeed.COOL_DOWN:
            return
        response = requests.get(self.url)
        root = ET.fromstring(response.text)

        point = 0
        for item in root[0].findall("item"):
            link = item.find("link").text
            if link not in self.seen_urls:
                point -= 1
                self.seen_urls.add(link)
                self.back_queue.append(link)

        self.point = self.point / 3 + (2 * (point)) / 3
        self.point = time.time()

    def fetch(self):
        if time.time() - self.last_visit < RssFeed.COOL_DOWN:
            return
        self.last_visit = time.time()

        if len(self.back_queue) == 0:
            return None

        link = self.back_queue.popleft()

        response = requests.get(link)
        content = BeautifulSoup(response.text, 'lxml').find("body").text
        title = BeautifulSoup(response.text, 'lxml').find("title").text

        print("{} -------> {}".format(self.url, link))
        return news_model.NewsModel(datetime.now().time(), title, link, "",
                          "", content, "")

    def fetch_and_update(self):
        self.update()
        self.fetch()

    def __lt__(self, other):
        return self.point < other.point


class Crawler:

    def __init__(self, urls):
        self.urls = urls

        self.front_queue = []
        for url in urls:
            self.front_queue.append(RssFeed(url))

        heapq.heapify(self.front_queue)

    def crawl(self):

        while True:
            rss_feed = heapq.heappop(self.front_queue)
            rss_feed.fetch_and_update()
            heapq.heappush(self.front_queue,rss_feed)




