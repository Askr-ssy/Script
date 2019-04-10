"""
Ac自动机-修改版(多模匹配)
适用于对某字符串同时匹配多个敏感词
运行时时间复杂度：O(n)

"""
from builtins import object

class State(object):
    __slots__=['symbol','id','transitions','parent','success','keyword','fail']

    def __init__(self,id,symbol=None,parent=None,success=False):
        self.symbol=symbol
        self.id=id
        self.transitions={}
        self.parent=parent
        self.success=success
        self.keyword=None
        self.fail=None

class KeyWordTree(object):

    def __init__(self):
        self._root_state=State(0)
        self._counter=1
        self._finalized=False

    def add(self,keyword):
        '''
        创建字典树
        '''
        if self._finalized:
            raise ValueError('KeyWordTree has been finalized')
        if len(keyword)<=0:
            return

        current_state=self._root_state  # 当前处理节点
        for char in keyword:
            if char in current_state.transitions:       # 循环到新建节点
                current_state=current_state.transitions[char]
            else:       # 新建子节点
                current_state.transitions[char]=State(self._counter,parent=current_state,symbol=char)
                current_state=current_state.transitions[char]
                self._counter+=1

        current_state.success=True
        current_state.keyword=keyword

    def finalize_fail(self):
        '''
        建立fail指针
        '''
        if self._finalized:
            raise ValueError('KeyWordTree has been finalized')
        
        self._root_state.fail=self._root_state
        self.search_fail_for_children(self._root_state)
        self._finalized=True

    def search_fail_for_children(self,root_state):
        processed=set()
        to_process=[root_state]

        while to_process:
            state=to_process.pop()
            processed.add(state.id)
            for child in state.transitions.values():
                if child.id not in processed:
                    self.search_fail(child)
                    to_process.append(child)
            
    def search_fail(self,state):
        '''
        查找当前节点的fail节点
        '''
        if state.fail:
            return
        parent=state.parent
        parent_fail=parent.fail
        while True:
            if state.symbol in parent_fail.transitions and parent_fail.transitions[state.symbol] != state:  # 如果当前节点在父节点的fail节点
                state.fail = parent_fail.transitions[state.symbol]                                          # 的fanil节点，并且不相等，设置其为当前节点fail节点
                break
            elif parent_fail == self._root_state:           # 父节点的fail节点为根节点
                state.fail = self._root_state               # 设置根节点为fail节点
                break
            else:
                parent_fail = parent_fail.fail              # 都不是则递归父节点的fail节点

        suffix = state.fail
        if suffix.fail is None:                 # 防止有fail指向None
            self.search_fail(suffix)

        for symbol, next_state in suffix.transitions.items():       # fail节点的子节点 引用到当前节点。无子节点
            if (symbol not in state.transitions and suffix != self._root_state):    
                state.transitions[symbol] = next_state

    def search_all(self,content):
        if not self._finalized:
            raise ValueError('KeyWordTree has not been finalized')
        
        current_state=self._root_state
        for idx,symbol in enumerate(content):
            current_state=current_state.transitions.get(
                symbol,self._root_state.transitions.get(symbol,
                                                        self._root_state
                )
            )
            state=current_state
            while state!=self._root_state:
                if state.success:   # 只要匹配到单词，并且非根节点
                    keyword=state.keyword  
                    yield (keyword,idx+1-len(keyword))
                state=state.fail

    def search_one(self,content):
        result=self.search_all(content)
        try:
            return next(result)
        except StopIteration:
            return None

    def search(self,content):
        return self.search_one(content)

if __name__ == "__main__":
    pass