from collections import UserDict


class Dictionary(UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            print("MISS: ##############################",
                  key, "##############################")
        else:
            return self.data[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item
