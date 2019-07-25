from multiprocessing import Process

from dump.rediscluster_test.IP维护.fff import RedisClient
from dump.rediscluster_test.IP维护.entrance import app
from dump.rediscluster_test.IP维护.getter import Getter
from dump.rediscluster_test.IP维护.check import Tester

class Scheduler:
    def schedule_tester(self, cycle=''):
        tester = Tester()
        while True:
            tester.run()

    def schedule_getter(self):
        getter = Getter()
        while True:
            getter.run()

    def schedule_api(self):
        app.run()

    def run(self):
        tester_process = Process(target=self.schedule_tester)
        tester_process.start()

        getter_process = Process(target=self.schedule_getter)
        getter_process.start()

        api_process = Process(target=self.schedule_api)
        api_process.start()



