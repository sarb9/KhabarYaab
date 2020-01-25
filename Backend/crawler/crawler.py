from extractor import RssFeed

RSS_FEEDS = ["https://www.tabnak.ir/fa/rss/allnews",
             "http://www.varzesh3.com/rss/all"]


def crawl():
    for rss in RSS_FEEDS:
        rss_feed = RssFeed(rss)



if __name__ == "__main__":
    