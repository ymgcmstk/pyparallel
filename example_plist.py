#!/usr/bin/env python
# -*- coding:utf-8 -*-

from parallel_toolbox import plist
import time
import os

def main_plist():
    hn = os.uname()[1]
    for i in plist(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'], verbose=True):
        print '[%s] %s' % (hn, i)
        time.sleep(1)
    return

if __name__ == '__main__':
    main_plist()
