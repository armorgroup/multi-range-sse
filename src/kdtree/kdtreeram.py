import random
import string
import math
import numpy as np
import os
import linecache


class Node(object):
    def __init__(self, dimension):
        self._key = None
        self._line = None
        self._l = None
        self._r = None
        self._P = None
        self._area = tuple([-math.inf, math.inf] * dimension)
        self._index = None


class KdTreeRam(object):
    def __init__(self, dimension):
        self._root = Node(dimension)
        self._range_query = []
        self._type = 'index'
        self.dimension = dimension

    def build(self, li):
        index = np.linspace(0, len(li) - 1, len(li), dtype=int)
        self._root = self.build_recur(li, 0, index)

    def build_recur(self, li, depth, index):
        if len(li) == 1:  # define leaf nodes that contain data
            node = Node(self.dimension)
            node._key = li[0]
            node._index = index[0]
            return node

        li_tmp = []

        for i in li:
            li_tmp.append(i[depth % self.dimension])

        middle = sorted(li_tmp)[len(li) // 2]

        left_li = []
        right_li = []
        left_idx = []
        right_idx = []

        for i, idx in zip(li, index):
            if i[depth % self.dimension] >= middle:
                right_li.append(i)
                right_idx.append(idx)
            if i[depth % self.dimension] < middle:
                left_li.append(i)
                left_idx.append(idx)

        middle_node = Node(self.dimension)
        middle_node._line = middle

        if left_li != []:
            middle_node._l = self.build_recur(left_li, depth + 1, left_idx)
        if right_li != []:
            middle_node._r = self.build_recur(right_li, depth + 1, right_idx)

        for i in range(self.dimension):
            if depth % self.dimension == i:
                imin, imax = middle_node._area[i * 2], middle_node._area[i * 2 + 1]
                if left_li != []:
                    middle_node._l._area = middle_node._l._area[:i * 2] + (imin, middle) + middle_node._l._area[i * 2 + 2:]
                if right_li != []:
                    middle_node._r._area = middle_node._r._area[:i * 2] + (middle, imax) + middle_node._r._area[i * 2 + 2:]

        return middle_node

    def intersect(self, a1, a2):
        cnd = []
        for i in range(self.dimension):
            cnd.append((a1[1 + 2 * i] < a2[0 + 2 * i] or a2[1 + 2 * i] < a1[0 + 2 * i]))
        if any(cnd):
            return False
        return True

    def query(self, area, type='index'):
        self._type = type
        self._range_query = []
        self.query_recur(self._root, area)
        return self._range_query

    def query_recur(self, node, area):
        if node == None:
            return
        if node._line == None:  # if it's a leaf node (a point)
            if node._key == None:
                return
            cnd = []
            for i in range(self.dimension):
                cnd.append((node._key[i] >= area[0 + 2 * i] and node._key[i] <= area[1 + 2 * i]))
            if all(cnd):
                if self._type == 'index':
                    self._range_query.append(node._index)
                elif self._type == 'point':
                    self._range_query.append(node._key)
            return

        if node._l != None:
            if self.intersect(area, node._l._area):
                self.query_recur(node._l, area)

        if node._r != None:
            if self.intersect(area, node._r._area):
                self.query_recur(node._r, area)