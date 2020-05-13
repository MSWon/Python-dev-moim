#팩토리 알고리즘

def facto(n):
    a=1
    for i in range(1,n+1):
        a=a*i
    return a


print (facto(3))    
