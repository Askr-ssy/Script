def LCS(a,b):
    if a=='' | b=='':
        pass
    pass

def Jaccardsimilarity(a,b):
    '''
    jaccard 系数
    '''
    if not a or not b:
        raise Exception('value error')
    if not isinstance(a,set):
        a=set(a)
    if not isinstance(b,set):
        b=set(b)
    return len((a.intersection(b)))/(len(b) if len(a)>len(b) else len(a))

def Edit_Distance(a,b):
    '''
    编辑距离
    '''
    if not a or not b:
        raise Exception('value error')
    disM=[[None for j in range(len(a)+1)] for i in range(len(b)+1)]
    print(disM)