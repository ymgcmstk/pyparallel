#!/usr/bin/env python
# -*- coding:utf-8 -*-

import inspect
import os
import random
import select
import socket
import sys
import threading

def textread(path):
    f = open(path)
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '').replace('\r', '')
    return lines

def textdump(path, lines):
    f = open(path, 'w')
    for i in lines:
        f.write(i + '\n')
    f.close()

def makedirs_if_missing(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def makebsdirs_if_missing(f_path):
    makedirs_if_missing(os.path.dirname(f_path) if '/' in f_path else f_path)

def location(depth=0):
    frame = inspect.currentframe(depth+1)
    return frame.f_lineno

class plistMaster(threading.Thread):
    keep_doing = True

    def __init__(self, server_sock, len_list, info_path, verbose):
        self._server_sock = server_sock
        self._len_list = len_list
        self._info_path = info_path
        self._verbose = verbose
        threading.Thread.__init__(self)

    def run(self):
        writefds = set()
        cur_ind = 0
        while self.keep_doing:
            conn, _ = self._server_sock.accept()
            writefds.add(conn)
            if len(writefds) > 0:
                wready = select.select([], writefds, [])[1]
            else:
                wready = set()
            for sock in wready:
                if cur_ind < self._len_list:
                    sock.send(str(cur_ind))
                    cur_ind += 1
                    if self._verbose:
                        print '[distribute_values]: %d / %d' % (cur_ind, self._len_list)
                sock.close()
                writefds.remove(sock)
                if cur_ind == self._len_list:
                    self.keep_doing = False
                    break
        if self._verbose:
            print '[distribute_values]: Finished.'
        for sock in writefds:
            sock.close()
        self._server_sock.close()
        os.remove(self._info_path)

# TODO: show speed when verbose is True
class plist(object):
    _is_master = None
    _master_server = None
    _master_port = None
    _bufsize = 4096
    _backlog = 10
    _mpm = None
    _info_path = None
    _temp_list_ind = None

    def __init__(self, targ_list, verbose=False):
        self._verbose = verbose
        self._targ_list = targ_list
        self._get_master_information()
        if self.is_master:
            # work as a master node
            self._start_thread()

    @property
    def is_master(self):
        if self._is_master is not None:
            return self._is_master
        self._is_master = False
        if not self._can_find_master(): # if cannot find master node
            self._is_master = True
        return self._is_master

    def _can_find_master(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self._master_server, self._master_port))
            self._temp_list_ind = int(sock.recv(self._bufsize))
            sock.close()
        except socket.error as err:
            if err.errno == 111:
                return False
            print err
            raise Exception('Unknown Error. Inspect err.')
        return True

    def _start_thread(self):
        # find a port number which is not being used
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
        self._master_server = socket.gethostname()
        self._master_port = cur_port

        # pack information and save as a file on self._info_path
        # - "tai 55555"
        textdump(self._info_path, ['%s %d' % (self._master_server, self._master_port)])

        # start thread
        self._mpm = plistMaster(server_sock, len(self._targ_list), self._info_path, self._verbose)
        self._mpm.start()

        # register function as excepthook for keyboardinterrupt
        cur_excepthook = sys.excepthook
        def kill_thread(*input1, **input2):
            cur_excepthook(*input1, **input2)
            self._mpm.keep_doing = False
            try:
                self.next()
            except StopIteration:
                pass
        sys.excepthook = kill_thread

    def __iter__(self):
        return self

    def next(self):
        if self._temp_list_ind is not None:
            list_ind = self._temp_list_ind
            self._temp_list_ind = None
            return self._targ_list[list_ind]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self._master_server, self._master_port))
            list_ind = int(sock.recv(self._bufsize))
        except socket.error as err:
            if err.errno == 111:
                raise StopIteration()
            print err
            raise Exception('Unknown Error. Inspect err.')
        sock.close()
        return self._targ_list[list_ind]

    def _get_master_information(self):
        cur_filename = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        cur_dirname = os.path.abspath(os.path.dirname(os.path.join(os.getcwd(), sys.argv[0])))
        self._info_path = os.path.join(cur_dirname, '.myparallel', '%s_%d.txt' % (cur_filename, location(2)))
        if not os.path.exists(self._info_path):
            makebsdirs_if_missing(self._info_path)
            self._is_master = True
            return
        file_content = textread(self._info_path)
        assert len(file_content) == 1
        self._master_server, self._master_port = file_content[0].strip().split()
        self._master_port = int(self._master_port)

class prange(plist):
    def __init__(self, *input1, **input2):
        super(prange, self).__init__(range(*input1, **input2))
