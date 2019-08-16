S='BBC ABCDAB ABCDABCDABDE'

P='ABCDABD'

def _index(S,P):
    def getNext(P):
        pLen=len(P)
        _next=[None]*pLen
        _next[0]=-1
        j=-1
        i=0 
        while j<pLen-1:
            if j==-1 or P[i]==P[j]:
                j+=1
                i+=1
                _next[i]=j
            else:
                j=_next[j]
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
