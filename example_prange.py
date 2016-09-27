#!/usr/bin/env python
# -*- coding:utf-8 -*-
from parallel_toolbox import prange
import time

def main_prange():
    for i in prange(30):
        print i
        time.sleep(1)
    return

if __name__ == '__main__':
    main_prange()
