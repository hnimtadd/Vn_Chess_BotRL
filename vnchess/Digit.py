import string
digs = string.digits + string.ascii_letters


def int2base(x, base, length):
    if x<0:
        sign = -1
    elif x==0:
        return digs[0]
    else:
        sign=1
    
    x*=sign
    digits=[]
    while x:
        digits.append(digs[int(x % base)])
        x=int(x/base)
    if sign < 0:
        digits.append('-')
    while len(digits) < length:
        digits.extend(["0"])
    return list(map(lambda x : int(x), digits))


if __name__ == "__main__":
    size=5
    validmoves=[[0,0,1,1],[0,0,0,0],[0,0,1,0],[0,0,0,1], [1,0,0,1]]
    start=[[0,1],[1,0],[1,1],[0,0],[4,4]]
    end = [[0,0],[0,]]

    print(validmoves)
    print("--"*20)
    for m in validmoves:
        i = m[0] +m[1]*size+m[2]*size**2 + m[3]*size**3
        print(i,":",int2base(i,size, 4))
