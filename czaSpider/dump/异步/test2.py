# import selectors
# import time
#
# from collections import deque
# def student(name, homeworks):
#     for homework in homeworks.items():
#         # time.sleep(1)
#         yield (name, homework[0], homework[1])  # 学生"生成"作业给老师
# class Teacher(object):
#     def __init__(self, students):
#         self.students = deque(students)
#     def handle(self):
#         """老师处理学生作业"""
#         while len(self.students):
#             student = self.students.pop()
#             try:
#                 homework = next(student)
#                 print('handling', homework[0], homework[1], homework[2])
#             except StopIteration:
#                 pass
#             else:
#                 self.students.appendleft(student)
#
#
# Teacher([
#     student('Student1', {'math': '1+1=2', 'cs': 'operating system'}),
#     student('Student2', {'math': '2+2=4', 'cs': 'computer graphics'}),
#     student('Student3', {'math': '3+3=5', 'cs': 'compiler construction'})
# ]).handle()

import time
import asyncio
import requests
async def spider(loop):
    # run_in_exectuor会返回一个Future，而不是coroutine object
    future1 = loop.run_in_executor(None, requests.get, 'https://www.python.org/')
    future2 = loop.run_in_executor(None, requests.get, 'http://httpbin.org/')
    print("hello?")
    # 通过命令行可以发现上面两个网络IO在并发进行
    print('!!!!')
    response1 = await future2  # 阻塞直到future1完成
    print("2222")
    response2 = await future1  # 阻塞直到future2完成
    print(len(response1.text), "1", time.time())
    print(len(response2.text), "2", time.time())
    return 'done'
loop = asyncio.get_event_loop()
# If the argument is a coroutine object, it is wrapped by ensure_future().
result = loop.run_until_complete(spider(loop))
print(result)
loop.close()