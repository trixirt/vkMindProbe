#!/usr/bin/python3
from os.path import dirname, realpath
import sys

d = dirname(dirname(realpath(__file__)))
sys.path.append(d)
print(d)

import ctypes
from vk import *
import pytest

def test_0():
    bufferSize = 512
    poison = 131
    expected = 0
    
    s = [ 4 * bufferSize ]
    v = vkc(s, d + "/../shader/memset.comp")
    p = v.maps()
    vk.memset(p[0], poison, s[0])
    v.unmap()
    v.run(bufferSize, 1, 1)

    u = void_to_uint32_t(p[0])
    for i in range(0, bufferSize):
        t = pauint32_t_getitem(u, i)
        assert t == expected

def test_1():
    bufferSize = 512
    poison = 131
    expected = 234

    p = new_puint32_t()
    puint32_t_assign(p, expected)
    spec = vkSpecialization()
    spec.append(p, 4, 0)
    spec.bind()
    
    s = [ 4 * bufferSize ]
    v = vkc(s, d + "/../shader/memset.comp", spec)
    p = v.maps()
    vk.memset(p[0], poison, s[0])
    v.unmap()
    v.run(bufferSize, 1, 1)

    u = void_to_uint32_t(p[0])
    for i in range(0, bufferSize):
        t = pauint32_t_getitem(u, i)
        assert t == expected

