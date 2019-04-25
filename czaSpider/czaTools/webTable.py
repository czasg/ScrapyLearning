# -*-coding:GBK -*-

import numpy as np

from scrapy import Selector

from czaSpider.czaTools.scraper import data_from_xpath
from czaSpider.czaTools.data_manipulation import strJoin


class _Td(object):
    """
    用于管理html中每一个td属性，
    包含简单的text文本内容，还有合并属性，暂未对其操作
    """
    rowspan = 1
    colspan = 1
    _content = None

    def __init__(self, content, rowspan, colspan):
        self._content = content
        if rowspan:
            self.rowspan = rowspan
        if colspan:
            self.colspan = colspan

    @classmethod
    def from_table(cls, td, get_content=None):  # instantiation
        content = get_content(td) if get_content else cls._get_content(td)
        rowspan = data_from_xpath(td, './@rowspan', first=True)
        colspan = data_from_xpath(td, './@colspan', first=True)
        return cls(content, rowspan, colspan)

    @property
    def text(self):
        return self._content

    @text.setter
    def text(self, content):
        self._content = content

    def strip(self, strict=False):  # strip each td content
        if strict:
            self._content = strJoin(self._content)
        else:
            self._content = self._content.strip()

    def _get_content(td):
        return data_from_xpath(td, './/text()', join=True)


class TableParser(object):
    """
    解析网页中的Table
    目前仅支持标准table，第一行为key，后序为value，或第一列为key，后序为value
    也可以指定key的起始下标
    """
    table = None

    def __init__(self, tr_td_array):
        self.tr_td_array = tr_td_array  # [tr, tr, [td,td,td..]..]

    @classmethod
    def from_html(cls, table, tr_xpath=None, td_xpath="./td", get_content=None):
        if isinstance(table, str):
            table = Selector(text=table).xpath('//body')
        cls.table = table

        trs = data_from_xpath(table, tr_xpath) if tr_xpath else \
            data_from_xpath(table, './tr') or data_from_xpath(table, './tbody/tr')

        return cls([[_Td.from_table(td, get_content) for td in data_from_xpath(tr, td_xpath)] for tr in trs])

    def transpose(self):
        self.tr_td_array = np.array(self.tr_td_array).transpose()
        return self

    def td_pipe(self, func, *args, **kwargs):
        self.tr_td_array = [[func(td, *args, **kwargs) for td in tr] for tr in self.tr_td_array]
        self.tr_td_array = [[td for td in tr if td] for tr in self.tr_td_array]
        self.tr_td_array = [tr for tr in self.tr_td_array if tr]
        return self

    def tr_pipe(self, func, *args, **kwargs):
        self.tr_td_array = [func(tr, *args, **kwargs) for tr in self.tr_td_array]
        self.tr_td_array = [tr for tr in self.tr_td_array if tr]
        return self

    def strip(self, strict=False):  # targeting text of td
        for tr in self.tr_td_array:
            for td in tr:
                td.strip(strict)
        return self

    def zip(self, key_index=0):
        if len(self.tr_td_array) < 2:
            print('this table just one line or lower, None values')
            return None
        tr_keys = self.tr_td_array[key_index: key_index + 1]
        tr_values = self.tr_td_array[key_index + 1:]

        keys = self._get_content_array(tr_keys, first=1)[0]
        values = self._get_content_array(tr_values)

        return [dict(zip(keys, value)) for value in values]

    def _get_content_array(self, tr_td_array, first=None):
        return [[td.text for td in tr] for tr in tr_td_array][:first]
