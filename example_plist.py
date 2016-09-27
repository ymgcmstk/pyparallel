#!/usr/bin/env python
# -*- coding:utf-8 -*-

from parallel_toolbox import plist
import time

def main_plist():
    for i in plist(['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko'], verbose=True):
        print i
        time.sleep(1)
    return

if __name__ == '__main__':
    main_plist()
