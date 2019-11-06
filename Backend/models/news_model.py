def create_models_list_from_news(news):
    return [NewsModel(*args) for args in news]


class NewsModel:

    __slots__ = ('id', 'publish_date', 'title', 'url', 'summary',
                 'meta_tags', 'content', 'thumbnail')
    typecode = 'd'
    gid = 0
    news = []

    def __init__(self, publish_date, title, url, summary,
                 meta_tags, content, thumbnail):
        self.publish_date = publish_date
        self.title = title
        self.url = url
        self.summary = summary
        self.meta_tags = meta_tags
        self.content = content
        self.thumbnail = thumbnail
        self.id = NewsModel.gid
        NewsModel.gid = NewsModel.gid + 1
        self.news.append(self)

    def __iter__(self):
        return (i for i in (self.publish_date, self.title, self.url, self.summary, self.meta_tags, self.content, self.thumbnail))

    def __str__(self):
        class_name = type(self).__name__
        return '{}({!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r})'.format(class_name, *self)
