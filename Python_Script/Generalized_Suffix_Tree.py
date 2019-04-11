# -*- coding: utf-8 -*-
"""
GST 广义后缀树
"""

class Node:
    def __init__(self,id,symbol=None,parent=None):
        self.symbol=symbol
        self.id=id
        self.next={}
        self.parent=parent
        self.generalized_idx={}
    
class Gst:
    def __init__(self):
        self._root_node=Node(0,'')
        self._count=1
    
    def add(self,keyword):
        for i in range(len(keyword),0,-1):
            self.build_branch(keyword[i-1:None])

    def build_branch(self,keyword):
        if len(keyword)<=0:
            return 
        
        current_node=self._root_node
        for char in keyword:
            if char in current_node.next:
                current_node=current_node.next[char]
            else:
                current_node.next[char]=Node(self._count,parent=current_node,symbol=char)
                current_node=current_node.next[char]
                self._count+=1

if __name__ == "__main__":
    gst=Gst()
    gst.add('abcdef')
    print(gst._root_node)



