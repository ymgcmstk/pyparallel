#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
from datetime import datetime
from time import sleep
from contextlib import closing
import sys
import os
import random

from parallel_toolbox import location, makebsdirs_if_missing, textdump, textread

def get_info_path(info_id):
    info_path = os.path.expanduser(os.path.join('~', '.myparallel', '%s_matserver.txt' % info_id))
    makebsdirs_if_missing(info_path)
    return info_path

def get_server_port(info_id):
    info_path = get_info_path(info_id)
    if os.path.exists(info_path):
        file_content = textread(info_path)
        assert len(file_content) == 1
        master_server, master_port = file_content[0].strip().split()
        master_port = int(master_port)
    else:
        master_server, master_port = None, None
    return master_server, master_port

def py_client(message, info_id):
    s = socket.socket()
    master_server, master_port = get_server_port(info_id)
    s.connect((master_server, master_port))
    s.send(message)
    new_message = s.recv(4096)
    s.close()
    return new_message


class MatServer(object):
    _get_flg = True
    _backlog = 10
    def __init__(self, info_id):
        self.s = socket.socket()

        for i in range(3):
            cur_port = random.randint(49200, 65500)
            try:
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.bind(('', cur_port))
                server_sock.listen(self._backlog)
                break
            except socket.error as err:
                if err.errno == 98:
                    continue
                print err
                raise Exception('Unknown Error. Inspect err.')
            if i == 2:
                raise Exception('Has reached maximum trial number.')
        self.s = server_sock
        self._master_server = socket.gethostname()
        if 'Mac' in self._master_server:
            self._master_server = '127.0.0.1'
        self._master_port = cur_port
        info_path = get_info_path(info_id)
        textdump(info_path, ['%s %d' % (self._master_server, self._master_port)])

    def get(self):
        assert self._get_flg
        self._get_flg = False
        s = self.s
        c, addr = s.accept()
        message = c.recv(4096)
        self.c = c
        return message

    def send(self, message):
        assert not self._get_flg
        self._get_flg = True
        c = self.c
        while True:
            try:
                c.send(message)
                break
            except:
                continue
        c.close()

def main_server():
    ms = MatServer('test')
    while True:
        message = ms.get()
        print message
        message += ' has been received.'
        ms.send(message)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main_server()
    else:
        print py_client(' '.join(sys.argv[1:]), 'test')
