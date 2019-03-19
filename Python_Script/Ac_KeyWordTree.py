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
        if self._finalized:
            raise ValueError('KeyWordTree has been finalized')
        if len(keyword)<=0:
            return

        current_state=self._root_state
        for char in keyword:
            if char in current_state.transitions:
                current_state=current_state.transitions[char]
            else:
                current_state.transitions[char]=State(self._counter,parent=current_state,symbol=char)
                current_state=current_state.transitions[char]
                self._counter+=1

        current_state.success=True
        current_state.keyword=keyword

    def finalize_fail(self):
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
        if state.fail:
            return
        parent=state.parent
        parent_fail=parent.fail
        while True:
            if state.symbol in parent_fail.transitions and parent_fail.transitions[state.symbol] != state:
                state.fail = parent_fail.transitions[state.symbol]   
                break
            elif parent_fail == self._root_state: 
                state.fail = self._root_state
                break
            else:
                parent_fail = parent_fail.fail       

        suffix = state.fail            
        if suffix.fail is None:       
            self.search_fail(suffix)

        for symbol, next_state in suffix.transitions.items():   
            if (symbol not in state.transitions and suffix != self._root_state):    
                state.transitions[symbol] = next_state
                print('test')  


        
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
                if state.success:
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