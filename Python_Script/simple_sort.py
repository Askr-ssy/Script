
def _bubble(a: list) -> list:
    """
    冒泡排序
    空间O(n)
    时间O(n!~n^2)
    """
    for i in range(1,len(a)):
        for j in range(i,0,-1):
            if a[j]<a[j-1]:
                a[j],a[j-1]=a[j-1],a[j]
    return a        
        


print(_bubble([6,5,4,3,2,1]))