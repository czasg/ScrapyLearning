import math
import random


class PageID(str):
    def __new__(cls):
        page_id = "".join(hex(math.floor(random.random() * 16))[2:] for _ in range(32))
        return super(PageID, cls).__new__(cls, page_id)
