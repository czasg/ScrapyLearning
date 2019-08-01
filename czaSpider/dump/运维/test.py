import psutil
import time

def get_cpu_info():
    print(psutil.cpu_count())  # CPU逻辑数量
    print(psutil.cpu_count(logical=False))  # CPU物理核心
    print(psutil.cpu_times())
    print(psutil.pids())  # 所有进程ID

    # p = psutil.Process(484)
    # print(p.name())
    # print(p.cpu_times())

    # p.terminate()   # 结束进程

    # "FineExec.exe", "FineExec.exe"，"FineReader.exe"
    import time
    pids = [psutil.Process(pid) for pid in psutil.pids()]
    for p in pids:
        print(time.time(), p.create_time(), p.name(), p.create_time(), p.cpu_times())
        # if p.name() == 'mongod.exe':
        #     print(p.kill())


def kill_pdf_process():
    current_time = time.time()
    pids = [psutil.Process(pid) for pid in psutil.pids()]
    for p in pids:
        if p.name() in ["FineExec.exe", "FineExec.exe", "FineReader.exe", "JSObjectAccessVB.exe"]:
            if (current_time - p.create_time()) > 60 * 10:
                p.kill()




if __name__ == '__main__':
    # get_cpu_info()
    kill_pdf_process()
"""
可以使用time.time和p.create_time进行对比，可以获取相关的时间
调用p.kill可以杀死进程
"""