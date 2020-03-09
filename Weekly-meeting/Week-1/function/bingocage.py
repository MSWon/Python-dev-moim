import random

class BingoCage:

    def __init__(self, items):
        self._items = list(items)  
        random.shuffle(self._items)

    def pick(self):  # <3>
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('datas are empty')

    def __call__(self):
        return self.pick()
