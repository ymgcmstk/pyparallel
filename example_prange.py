#!/usr/bin/env python
# -*- coding:utf-8 -*-
from parallel_toolbox import prange
import os
import time

def main_prange():
    hn = os.uname()[1]
    for i in prange(10):
        print '[%s] %d' % (hn, i)
        time.sleep(1)
    return

if __name__ == '__main__':
    main_prange()
