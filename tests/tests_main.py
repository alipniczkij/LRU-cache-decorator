#!/usr/bin/env python
# coding: utf-8

import random
import time

from lru_cache.main import LRUCacheDecorator

def test_lrucache_01():
    @LRUCacheDecorator(maxsize=3, ttl=None)
    def get_sq(s):
        time.sleep(2)
        return s ** 2

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start > 0.5

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5


def test_lrucache_02():
    @LRUCacheDecorator(maxsize=3, ttl=None)
    def get_sq(s):
        time.sleep(2)
        return s ** 2

    get_sq(1)
    get_sq(2)
    get_sq(3)
    get_sq(1)
    get_sq(4)
    get_sq(5)

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5


def test_lrucache_03():
    @LRUCacheDecorator(maxsize=4, ttl=None)
    def get_sq(s):
        time.sleep(1)
        return s ** 2

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start > 0.5
    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5
    l = [5, 6, 7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5
    l = [1, 5, 6, 7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [7, 5, 6, 1]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [15]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5
    l = [1, 6, 5, 15]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start < 0.5
    l = [7]
    for i in l:
        t_start = time.time()
        get_sq(i)
        assert time.time() - t_start > 0.5


def test_lrucache_04():
    my_global_vars = {}
    @LRUCacheDecorator(maxsize=3, ttl=10)
    def get_sq(s):
        time.sleep(2)
        nonlocal my_global_vars
        my_global_vars[s] = s ** 2
        return my_global_vars[s]

    get_sq(3)
    t_start = time.time()
    get_sq(3)
    assert time.time() - t_start < 2
    assert my_global_vars[3] == get_sq(3) == 9

    for i in my_global_vars:
        my_global_vars[i] += 1

    t_start = time.time()
    get_sq(3)
    assert time.time() - t_start < 2
    assert my_global_vars[3] != get_sq(3)

    time.sleep(10)
    get_sq(3)
    assert my_global_vars[3] == get_sq(3)