# -*- coding: utf-8 -*-
import os

desktop = r'C:\\Users\\czaOrz\\Desktop'

if __name__ == '__main__':
    pdf = desktop + r'\\1.pdf'
    output = desktop + r'\\1.html'
    cmd = 'FineCmd ' + pdf + ' /lang Mixed /out ' + output +' /quit'
    print(cmd)
    os.system(cmd)