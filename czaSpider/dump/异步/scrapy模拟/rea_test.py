import unittest

from HtmlTestRunner import HTMLTestRunner  # pip install html-testRunner

import rea

"""
新版rea测试用例
解决旧版中存在的特例，如：\(\)、(?:)、(?=)、(?!)等导致的返回结果数量异常
此次使用 re.compile(pattern, flags).groups 代替旧版根据 '(' 的个数返回值
"""


class TestRea(unittest.TestCase):
    def test1(self):
        res1 = rea.search('(\d+)', '').group(1)
        res2 = rea.search('(\d+)', '').groups()
        self.assertEqual(res1, None, msg='测试空字符串 + group(1)成功')
        self.assertEqual(res2, (None,), msg='测试空字符串 + groups()成功')

    def test2(self):
        res = rea.search('(?:)(\d+)(?=)', '').groups()
        self.assertEqual(res, (None,), msg='测试 (?:)/()/(?=) 成功')

    def test3(self):
        res1 = rea.search('\(\)(\d+)\(\)(\d+)', '').group(1)
        res2 = rea.search('\(\)(\d+)\(\)(\d+)', '').groups()
        self.assertEqual(res1, None, msg='测试 \(\)(\d+)\(\)(\d+) + group(1)成功')
        self.assertEqual(res2, (None, None,), msg='测试 \(\)(\d+)\(\)(\d+) + groups()成功')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRea))

    runner = HTMLTestRunner(output='result')
    runner.run(suite)
