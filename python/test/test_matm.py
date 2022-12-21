#!/usr/bin/python3
from os.path import dirname, realpath
import sys

d = dirname(dirname(realpath(__file__)))
sys.path.append(d)
print(d)

import numpy as np
import ctypes
from vk import *
import pytest

def test_0():
    k = 40
    m = 96
    n = 20
    
    params = [ m, k, k, n ]
    P = np.array(params, np.uintc)
    A = np.random.randn(m, k).astype(np.float32)
    B = np.random.randn(k, n).astype(np.float32)
    C = np.zeros((m, n), np.float32)
    E = np.zeros((m, n), np.float32)
    np.matmul(A, B, E)
    
    T = np.zeros((m, n), np.float32)
    s = [ A.size*A.itemsize, B.size*B.itemsize, C.size*C.itemsize, P.size*P.itemsize]
    v = vkc(s, d + "/../shader/matm.comp")
    p = v.maps()
    vk.memcpy(p[0], vk.pointer(A.ctypes.data), s[0])
    vk.memcpy(p[1], vk.pointer(B.ctypes.data), s[1])
    vk.memcpy(p[3], vk.pointer(P.ctypes.data), s[3])
    v.unmap()
    v.run(m, n, 1)
    vk.memcpy(vk.pointer(C.ctypes.data), p[2], s[2])
    D = np.subtract(E, C)
    s = np.absolute(np.sum(D))
    print(s)
    assert s < 0.1
