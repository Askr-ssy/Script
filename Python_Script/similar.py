def LCS(a,b):
    if a=='' | b=='':
        pass
    pass

def Edit_Distance(a,b):
    '''
    编辑距离
    '''
    if not a or not b:
        raise Exception('value error')
    disM=[[None for j in range(len(a)+1)] for i in range(len(b)+1)]
    print(disM)