# encoding: utf-8

import os, sys
import xlrd, xlwt
from xlutils.copy import copy
from lxml.html import etree, open_in_browser

from czaSpider.czaTools.path_func import to_path
from czaSpider.czaTools.process_dict import arrayJoin


def array2excel(array, fileName, sheetName):
    ExcelWriter(fileName, sheetName).array2excel(array).save()


class ExcelWriter(object):
    """
    write an array to excel.
    you must input fileName, sheetName and what array you want to write.
    each sub is one row, and sub-sub is each col.
    if excel exist and as to sheetName, then append this array to the last
    """

    def __init__(self, fileName, sheetName, path=''):
        self.fileName = self.check_suffix(fileName)
        self.sheetName = sheetName
        self.save_path = to_path(path, self.fileName) if path else self.fileName
        self.row_index = 0
        self.col_index = 0
        self.xlsWB = copy(self.load_excel(self.save_path, sheetName))
        try:
            self.sheet = self.xlsWB.get_sheet(sheetName)
        except:
            self.sheet = self.xlsWB.add_sheet(sheetName)

    def load_excel(self, filePath, sheetName):
        check = os.path.exists(filePath)
        if check:
            print("文件已存在，使用默认文件进行读写")
            return self._get_nrows_and_ncols(xlrd.open_workbook(filePath), sheetName)
        else:
            print("文件不存在，新建中...")
            try:
                self._create_excel(filePath, sheetName)
            except:
                raise Exception("创建出错！")
            else:
                print("新建成功！")
                return self._get_nrows_and_ncols(xlrd.open_workbook(filePath), sheetName)

    def _create_excel(self, filePath, sheetName):
        wb = xlwt.Workbook()
        wb.add_sheet(sheetName)
        wb.save(filePath)

    def _get_nrows_and_ncols(self, ow, sheetName):
        sheet = ow.sheet_by_name(sheetName)
        self.nrows = sheet.nrows
        self.ncols = sheet.ncols
        return ow

    def check_suffix(self, fileName):
        if '.' in fileName:
            if not fileName.endswith((".xls", ".xlsx")):
                raise ValueError("请输入正确的文件名，如'xxx'或'xxx.xls'或'xxx.xlsx'")
            else:
                return fileName
        else:
            return fileName + ".xls"

    def cursor_move(self, right=False, left=False, up=False, down=False):
        if right:
            self.col_index += 1
        if left:
            self.col_index -= 1
        if up:
            self.row_index -= 1
        if down:
            self.row_index += 1

    def cursor_jump(self, row_index, col_index):
        self.row_index = row_index
        self.col_index = col_index

    def cursor_enter(self, col_index=None):
        self.cursor_move(down=True)
        self.cursor_jump(self.row_index, col_index or 0)

    def write(self, value, row_index=None, col_index=None):
        r = row_index or self.row_index
        c = col_index or self.col_index
        self.sheet.write(r, c, value)

    def array2excel(self, array):
        self.row_index = self.nrows
        in_nrows = len(array)
        count = 0
        for i in range(self.row_index, self.row_index + in_nrows):
            for value in array[count]:
                self.write(value)
                self.cursor_move(right=True)
            self.cursor_enter()
            count += 1
        return self

    def table_to_excel(self, html_table):
        pass  # todo, maybe need this function

    def save(self):
        self.xlsWB.save(self.save_path)
        print("write array done and save success")


class _Td(object):
    _merged = False
    row_span = 1
    col_span = 1

    def __init__(self, content, ctype):
        self.content = content
        self.ctype = ctype

    @classmethod
    def from_cell(cls, cell):
        return cls(cell.value, cell.ctype)

    @property
    def merged(self):
        return self._merged

    @merged.setter
    def merged(self, flags):
        self._merged = flags

    @property
    def value(self):
        return self.content

    @value.setter
    def value(self, content):
        self.content = content

    def set_span(self, row, rows, col, cols):
        self.row_span = rows - row
        self.col_span = cols - col

    def to_html(self):
        if self.merged:
            return
        _attribute = []
        if self.row_span > 1:
            _attribute.append(' rowspan="{}"'.format(self.row_span))
        if self.col_span > 1:
            _attribute.append(' colspan="{}"'.format(self.col_span))
        return "<td{attribute}>{value}</td>".format(attribute=arrayJoin(_attribute), value=self.value)


class _Sheet(object):
    def __init__(self, sheet):
        self.sheet = sheet
        self.tr_td_array = [[_Td.from_cell(cell) for cell in sheet.row(i)] for i in range(sheet.nrows)]
        self._set_span()

    def _set_span(self):
        for row, rows, col, cols in self.sheet.merged_cells:
            for i in range(row, rows):
                for j in range(col, cols):
                    if i == row and j == col:
                        self.tr_td_array[i][j].set_span(row, rows, col, cols)
                        continue
                    self.tr_td_array[i][j].merged = True

    def to_html(self):
        td_td_html = [[td.to_html() for td in tr] for tr in self.tr_td_array]
        td_td_html = [arrayJoin(tr) for tr in td_td_html if tr]
        td_td_html = ["<tr>{}</tr>".format(tr) for tr in td_td_html]
        return arrayJoin(td_td_html)

    def to_array(self):
        tr_td_array = [[td.value for td in tr] for tr in self.tr_td_array]
        tr_td_array = [tr for tr in tr_td_array if tr]
        return tr_td_array

    def open_in_browser(self):
        if sys.platform == "win32":
            try:
                td_td_html = self.to_html()
                if not td_td_html:
                    return
                table = """<table border="1" cellspacing="0">{}</table>""".format(td_td_html)
                open_in_browser(etree.fromstring(table))
            except:
                print("open_in_browser ERROR!")
            else:
                print("open in browser success!")
        else:
            print("{}不支持此功能".format(sys.platform))


class ExcelReader(object):
    def __init__(self, workbook):
        self.wb = workbook

    @classmethod
    def from_excel(cls, file):
        if isinstance(file, str):
            return cls(xlrd.open_workbook(file, formatting_info=True))
        elif isinstance(file, bytes):
            return cls(xlrd.open_workbook(file_contents=file, formatting_info=True))

    def sheets(self, func, sheetName=None, sheetIndex=None) -> dict:
        if sheetName:
            sheets = [self.wb.sheet_by_name(sheetName)]
        elif sheetIndex:
            sheets = [self.wb.sheet_by_index(sheetIndex)]
        else:
            sheets = self.wb.sheets()
        res_dict = {sheet.name: func(_Sheet(sheet)) for sheet in sheets}
        res_dict = {key: value for key, value in res_dict.items() if value}
        return res_dict

    def to_html(self, **kwargs):
        return self.sheets(lambda x: x.to_html(), **kwargs)

    def to_array(self, **kwargs):
        return self.sheets(lambda x: x.to_array(), **kwargs)

    def open_in_browser(self, **kwargs):
        return self.sheets(lambda x: x.open_in_browser(), **kwargs)


if __name__ == "__main__":
    # ExcelWrite('test.xls', 'test').array_to_excel([[1, 2, 3], [4, 5, 6], [7,8,9,10]]).save()
    # todo, test here about excel reader function
    from czaSpider.test_set import get_test_path
    test_sets = get_test_path(__file__)
    for test in test_sets:
        print(ExcelReader.from_excel(test).to_html())
        # print(ExcelReader.from_excel(test).to_array())
        # ExcelReader.from_excel(test).open_in_browser()
    pass
