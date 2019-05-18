import os

STORE_PATH = os.sep.join((os.path.dirname(os.path.abspath(__file__)), "test"))

def toPath(fileName):
    return os.path.join(STORE_PATH, fileName)

# print(STORE_PATH)

# with open(os.sep.join((STORE_PATH,"test.txt")), 'wb') as f:
#     f.write(b'hello world')
# print(toPath('test'))