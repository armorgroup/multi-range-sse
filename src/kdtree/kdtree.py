import random
import string
import math
import numpy as np
import os
import linecache




class Node(object):
    def __init__(self):
        self._key = None
        self._line = None
        self._l = None
        self._r = None
        self._P = None
        self._area = tuple([-math.inf,math.inf]*4)
        self._index = None
        self._lpnt=None
        self._rpnt=None
        
        
class KdTree(object):
    def __init__(self, dir_kdtree):
        self._root = Node()        
        # universe_node = Node()   # we dont need this for now, keep it for now     
        # self._root._p = universe_node  # we dont need this for now, keep it for now 
        self._range_query = []
        self._leaf = 0
        self._type = 'index'
        self.dir_kdtree= dir_kdtree
        self._lncnt=1
        

    def build(self,li):
        # if not os.path.exists(self.dir_kdtree): 
        with open(self.dir_kdtree, 'w'):
            pass
        with open(self.dir_kdtree, "a") as file:                 
            index = np.linspace(0, len(li)-1, len(li), dtype=int)  
            self._root = self.build_recur(li, 0, index,file)            
            self._root._lpnt=self._lncnt-2
            self._root._rpnt=self._lncnt-1
            self._write_node(self._root,file) 
    def build_recur(self,li,depth, index,file):
        
        if len(li) == 1: # define leaf nodes that contains data
            node = Node()
            node._key = li[0]
            node._index = index[0]
            # self._write_node(node,file)
            return node
        
        li_tmp = []
        for i in li:
            li_tmp.append(i[depth % 4])
        
        # index = np.argsort(li_tmp)[len(li)//2]    
        middle = sorted(li_tmp)[len(li)//2] # sorted(li_tmp)[len(li)//2] #kselect(li_tmp,len(li)//2+1)
        
        
        left_li = []
        right_li = []
        left_idx = []
        right_idx = []
 
        for i, idx in zip(li, index):
            if i[depth % 4] >= middle:
                right_li.append(i)
                right_idx.append(idx)
            if i[depth % 4] < middle:
                left_li.append(i)
                left_idx.append(idx)
        middle_node = Node()
        middle_node._line = middle


        if left_li != []:
            middle_node._l = self.build_recur(left_li,depth + 1, left_idx,file)            
        if right_li != []:
            middle_node._r = self.build_recur(right_li,depth + 1, right_idx,file)            
        if depth % 4 == 0:
            imin,imax,jmin,jmax,kmin,kmax,mmin,mmax = middle_node._area
            if left_li != []:
                middle_node._l._area = (imin,middle,jmin,jmax,kmin,kmax,mmin,mmax)
            if right_li != []:
                middle_node._r._area = (middle,imax,imin,imax,kmin,kmax,mmin,mmax)
        elif depth % 4 == 1:
            imin,imax,jmin,jmax,kmin,kmax,mmin,mmax = middle_node._area
            if left_li != []:
                middle_node._l._area = (imin,imax,jmin,middle,kmin,kmax,mmin,mmax)
            if right_li != []:
                middle_node._r._area = (imin,imax,middle,jmax,kmin,kmax,mmin,mmax)
        elif depth % 4 == 2:
            imin,imax,jmin,jmax,kmin,kmax,mmin,mmax = middle_node._area
            if left_li != []:
                middle_node._l._area = (imin,imax,jmin,jmax,kmin,middle,mmin,mmax)
            if right_li != []:
                middle_node._r._area = (imin,imax,jmin,jmax,middle,kmax,mmin,mmax)
        elif depth % 4 == 3:
            imin,imax,jmin,jmax,kmin,kmax,mmin,mmax = middle_node._area
            if left_li != []:
                middle_node._l._area = (imin,imax,jmin,jmax,kmin,kmax,mmin,middle)
            if right_li != []:
                middle_node._r._area = (imin,imax,jmin,jmax,kmin,kmax,middle,mmax)
        
        middle_node._lpnt=self._lncnt
        self._write_node(middle_node._l,file)        
        middle_node._rpnt=self._lncnt
        self._write_node(middle_node._r,file)        
        return middle_node

    def intersect(self,a1,a2):
        cnd = []
        for i in range(4):
            cnd.append((a1[1+2*i]<a2[0+2*i] or a2[1+2*i]<a1[0+2*i]))
        if any(cnd):
            return False
        return True
    
    def query(self,area,type='index'):        
        self._type = type
        self._range_query = []
        with open(self.dir_kdtree, 'r') as fp:
            rootln = len(fp.readlines())
        self._root=self._parse_node(rootln)
        self.query_recur(self._root,area)
        return self._range_query
    
    def query_recur(self,node,area):
        if node == None:
            return
        if node._line == None: # if it's a leaf node a.k.a a point
            if node._key == None:
                return
            cnd = []
            for i in range(4):
                cnd.append((node._key[i] >= area[0+2*i] and node._key[i] <= area[1+2*i]))
            if all(cnd):
                if self._type == 'index':
                    self._range_query.append(node._index)
                elif self._type == 'point':                    
                    self._range_query.append(node._key)
            return
        
        if node._lpnt:
            node._l=self._parse_node(node._lpnt)
        else:
            node._l=None       

        if node._l != None:
            if self.intersect(area,node._l._area):
                self.query_recur(node._l,area)
        
        if node._rpnt:
            node._r=self._parse_node(node._rpnt)
        else:
            node._r=None

        if node._r != None:
            if self.intersect(area,node._r._area):   
                self.query_recur(node._r,area)
        

    # def count_leaf(self):
    #     self._leaf = 0
    #     self.count(self._root)
    #     return self._leaf
    # def count(self,node):
    #     if node == None:
    #         return
    #     if node._key != None:
    #         self._leaf +=1
        
    #     self.count(node._l)
    #     self.count(node._r)

    def _write_node(self, Node,file):
        if Node:
            node_data=[Node._key, Node._line, Node._area, Node._index, Node._lpnt, Node._rpnt]
        else:
            node_data=[None]*6
            node_data[2]=tuple([-math.inf,math.inf]*4)   
        node_data=[str(i) for i in node_data]
        node_data='\t'.join(node_data)
        node_data=node_data+'\n'      
        file.write(node_data)
        self._lncnt+=1    
    
    def _parse_node(self, lineNum:int)->Node:               
        linedata = linecache.getline(self.dir_kdtree, lineNum).strip().split('\t')        
        linedata=[None if i=='None' else i for i in linedata]
        if linedata[0]:
            linedata[0]=[int(i) for i in linedata[0][1:-1].split(', ')]
        if linedata[1]:
            linedata[1]=int(linedata[1])
        if linedata[2]:
            linedata[2]=linedata[2][1:-1].split(', ')
            for i,value in enumerate(linedata[2]):
                if value=='inf':
                    linedata[2][i]=math.inf
                elif value=='-inf':
                    linedata[2][i]=-math.inf
                else:         
                    linedata[2][i]=int(value)
            linedata[2]=tuple(linedata[2])
        linedata[3:]=[i if i==None else int(i) for i in linedata[3:]]
        node=Node()
        node._key, node._line, node._area, node._index, node._lpnt, node._rpnt=linedata
        return node
                



        



    


            
 
 





