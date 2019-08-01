import psutil

def kill_pdf_process():
    pids = [psutil.Process(pid) for pid in psutil.pids()]
    for p in pids:
        if p.name() in ["FineExec.exe", "FineExec.exe", "FineReader.exe"]:
            p.kill()


if __name__ == '__main__':
    kill_pdf_process()
