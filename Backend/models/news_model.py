def create_models_list_from_news(news, labeled_data=False):
    if labeled_data:
        return [LabeledNewsModel(news_obj[0], news_obj[7], news_obj[8]) for news_obj in news]
    else:
        return [NewsModel(args['publish_date'], args['title'], args['url'], args['summary'],
                          args['meta_tags'], args['content'], args['thumbnail']) for index, args in news.iterrows()]


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
        return (i for i in
                (self.publish_date, self.title, self.url, self.summary, self.meta_tags, self.content, self.thumbnail))

    def __str__(self):
        class_name = type(self).__name__
        return '{}({!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r}\n, {!r})'.format(class_name, *self)


class LabeledNewsModel:

    def __init__(self, id, content, category):
        self.id = id
        self.category = category
        self.content = content
