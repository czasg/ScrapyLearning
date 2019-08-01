# -*- coding: utf-8 -*-
import os
import time
import psutil

desktop = r'C:\\Users\\czaOrz\\Desktop'


def kill_pdf_process():
    current_time = time.time()
    pids = [psutil.Process(pid) for pid in psutil.pids()]
    for p in pids:
        if p.name() in ["FineExec.exe", "FineReader.exe", "JSObjectAccessVB.exe"] \
                and (current_time - p.create_time()) > 5:
            p.kill()


if __name__ == '__main__':
    pdf = desktop + r'\\1.pdf'
    output = desktop + r'\\1.html'
    cmd = 'FineCmd ' + pdf + ' /lang Mixed /out ' + output + ' /quit'
    print(cmd)
    os.system(cmd)
