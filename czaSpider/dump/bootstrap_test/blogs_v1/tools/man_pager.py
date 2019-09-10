def get_page_index(page_str):
    p = 1
    page_str = page_str[0] if isinstance(page_str, list) else page_str
    try:
        p = int(page_str)
    except:
        pass
    return 1 if p < 1 else p


def get_page_size(page_str):
    p = 6
    page_str = page_str[0] if isinstance(page_str, list) else page_str
    try:
        p = int(page_str)
    except:
        pass
    return 6 if p < 6 else p


class Pager:
    def __init__(self, item_count, page_index=1, page_size=6):
        self.item_count = item_count
        self.page_size = page_size
        self.page_count = item_count // page_size + (1 if item_count % page_size > 0 else 0)
        if (item_count == 0) or (page_index > self.page_count):
            self.page_index = 1
            self.offset = 0
            self.limit = 0
        else:
            self.page_index = page_index
            self.offset = self.page_size * (page_index - 1)
            self.limit = self.page_size
        self.has_next = self.page_index < self.page_count
        self.has_previous = self.page_index > 1

    def __str__(self):
        return 'item_count: %s, page_count: %s, page_index: %s, page_size: %s, offset: %s, limit: %s' % \
               (self.item_count, self.page_count, self.page_index, self.page_size, self.offset, self.limit)

    __repr__ = __str__
