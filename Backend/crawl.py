from crawler.crawler import RSS_FEEDS, Crawler

if __name__ == "__main__":
    crawler = Crawler(RSS_FEEDS)
    crawler.crawl()
