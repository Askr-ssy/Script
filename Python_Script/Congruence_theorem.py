import math 
def congruence(*args,**kwargs):
    a=args[0]
    b=args[1]
    m=args[2]
    return m%(a-b)==0

if __name__ == "__main__":
    print(congruence(13,17,2))