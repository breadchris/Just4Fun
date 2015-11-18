import random
t=open(__file__).read()
b={True:False,False:True}
def s(i):return(i+s(i-1) if i else 0)
g=int(raw_input("What is the secret number? "))
print("Nah" if g!=random.randrange(s(954)) else (t[23]+t[25]+t[33]+t[102]+t[40]+t[5]+t[120]+t[202]+t[21]+t[185]+t[43]+t[1]+t[22]+t[220]+t[163]+t[27]+t[0]+t[5]+t[49]+t[28]+t[2]+t[226]+t[4]+t[5]+t[49]+t[62]))
