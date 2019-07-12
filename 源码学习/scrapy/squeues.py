"""
Scheduler queues
"""

import marshal
from six.moves import cPickle as pickle

from queuelib import queue

def _serializable_queue(queue_class, serialize, deserialize):

    class SerializableQueue(queue_class):

        def push(self, obj):
            s = serialize(obj)
            super(SerializableQueue, self).push(s)

        def pop(self):
            s = super(SerializableQueue, self).pop()
            if s:
                return deserialize(s)

    return SerializableQueue

def _pickle_serialize(obj):
    try:
        return pickle.dumps(obj, protocol=2)  # 序列化，不需要写到文件中
    # Python <= 3.4 raises pickle.PicklingError here while
    # 3.5 <= Python < 3.6 raises AttributeError and
    # Python >= 3.6 raises TypeError
    except (pickle.PicklingError, AttributeError, TypeError) as e:
        raise ValueError(str(e))

PickleFifoDiskQueue = _serializable_queue(queue.FifoDiskQueue, \
    _pickle_serialize, pickle.loads)
PickleLifoDiskQueue = _serializable_queue(queue.LifoDiskQueue, \
    _pickle_serialize, pickle.loads)
MarshalFifoDiskQueue = _serializable_queue(queue.FifoDiskQueue, \
    marshal.dumps, marshal.loads)
MarshalLifoDiskQueue = _serializable_queue(queue.LifoDiskQueue, \
    marshal.dumps, marshal.loads)
FifoMemoryQueue = queue.FifoMemoryQueue
LifoMemoryQueue = queue.LifoMemoryQueue

"""
class queue.Queue(maxsize)          # Python queue模块的FIFO队列先进先出。
class queue.LifoQueue(maxsize)       # LIFO类似于堆，即先进后出。
class queue.PriorityQueue(maxsize)    # 还有一种是优先级队列级别越低越先出来
"""

"""
常用的两种序列化模块json和pickle

json.loads()
json.dumps()
pickle.dumps(obj)：以字节对象形式返回封装的对象，不需要写入文件中
pickle.loads(bytes_object): 从字节对象中读取被封装的对象，并返回

json.load()
json.dump()
pickle.dump(obj, file, protocol=None,)
pickle.load(file,*,fix_imports=True, encoding="ASCII", errors="strict")

"""