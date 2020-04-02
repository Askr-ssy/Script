def Jaccardsimilarity(a, b):
    '''
    jaccard 系数
    '''
    if not a or not b:
        raise Exception('value error')
    if not isinstance(a, set):
        a = set(a)
    if not isinstance(b, set):
        b = set(b)
    return len((a.intersection(b)))/(len(b) if len(a) > len(b) else len(a))
