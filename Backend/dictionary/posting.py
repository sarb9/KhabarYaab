from collections import UserList, namedtuple

Posting = namedtuple('Posting', ['doc_id', 'position'])


class PostingList(UserList):

    def __init__(self):
        self.df = 0
        super().__init__()

    def append(self, pl):
        self.data.append(pl)
        self.df += pl.df

    def add_posting(self, ps):
        self.data.append(ps)

    def __str__(self):
        return str(self.data)
