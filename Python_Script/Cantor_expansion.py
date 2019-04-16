"""
康托展开和逆康托展开
"""
import math

def cantor(*args,**kwargs):
    lis=args[0]
    if isinstance(lis,int):
        lis=list(map(int, str(lis)))
    
    n=len(lis)
    sum=0

    for i in range(0,n):
        count=0
        for j in range(i,n):
            if lis[j]<lis[i]:
                count+=1
        sum+=count*math.factorial(n-i-1)
        print(sum,n-i-1)
    return sum

def uncantor(*args,**kwargs):
    rank=args[0]
    sets=args[1]
    sets=sorted(sets)
    n=len(sets)
    _the_return=''

    rank-=1 # 从零开始
    
    for i in range(0,len(sets)):
        char=sets[int(rank/math.factorial(n-i-1))]
        sets.remove(char)
        _the_return+=str(char)
        rank=rank%math.factorial(n-i-1)
    return _the_return


if __name__ == "__main__":
    print(cantor(31452)+1)
    # print(uncantor(cantor(31452)+1,{1,2,3,4,5}))