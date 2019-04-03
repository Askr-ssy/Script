import math 
def congruence(*args,**kwargs):
    a=args[0]
    b=args[1]
    m=args[2]
    return m%(a-b)==0

def powmod(*args,**kwargs):
    '''
    n^b mod c
    '''
    a=args[0]
    b=args[1]   
    c=args[2]
    if b==0:
        return 1
    if b==1:
        return a%c
    temp=powmod(a,b>>1,c)
    temp=temp*temp%c
    if b %2:
           temp=temp*a%c%c
    return temp
if __name__ == "__main__":
    print(congruence(13,17,2))
    print(powmod(11,12345,12345))