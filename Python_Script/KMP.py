S='BBC ABCDAB ABCDABCDABDE'

P='ABCDABD'

def _index(S,P):
    def getNext(P):
        pLen=len(P)
        _next=[None]*pLen
        _next[0]=-1                     # 1 断言：在J=0的时候，值为-1
        k=-1        # K为当前失败后，下一步要跳到的位置
        j=0         # J为next数组中的索引
        while j<pLen-1:                 
            if k==-1 or P[j]==P[k]:     # 2.1.1 当P[J]==P[K] 即,前缀与后缀相同时
                k+=1
                j+=1
                _next[j]=k              # 2.1.2 P[J+1] 与 P[K+1] 成立
            else:                       # 2.2.1 当P[J] != P[k] 时,即 前缀与后缀不同
                k=_next[k]              # 2.2.2 最长前缀后缀匹配失败时,K通过next数组跳到失败的位置 成立
        return _next
    
    _next=getNext(P)
    sLen=len(S)
    pLen=len(P)

    i=0             # 主字符串的标志位
    j=0             # 模式字符串的标志位

    while i<sLen and j <pLen:
        if j==-1 or S[i]==P[j]:
            i+=1
            j+=1
        else:
            j=_next[j]
    if j==pLen:
        return i-j
    else:
        return -1