#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import sys
import scipy.io as sio
from mat_server import get_server_port
import random

def py_client(data, info_id):
    s = socket.socket()
    master_server, master_port = get_server_port(info_id)
    base_fname = str(random.randint(0,1000000000)) + '.mat'
    fname = os.path.abspath(base_fname)
    sio.savemat(fname, {'data': data})
    s.connect((master_server, master_port))
    s.send(fname)
    new_message = s.recv(4096)
    s.close()
    os.remove(fname)
    return new_message

if __name__ == '__main__':
    import numpy as np
    data = np.arange(5, dtype=np.int64)
    print 'data:', data
    print 'answer:', data.sum()
    print 'returned:', py_client(data, 'MatDataServerTest')
