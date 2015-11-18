import random

x = "deadbeefcafebab3:loolmonyytcrackr:1234098710101100:asdfhjklqwertyui:sinoonymfortehwn"

parts = x.split(":")

ord_parts = []
for part in parts:
    ord_parts.append([ord(_) for _ in part])

'''
print "if",
for i in range(len(ord_parts)):
    print "_[%d] !=" % i, sum(ord_parts[i]), "or",
print "\n\texit(-1)"
'''

operations = ["-", "+", "*", "^", "/", "%"]

#print "if",
for s1, s2 in [(random.choice(range(0, len(ord_parts))), random.choice(range(0, len(ord_parts)))) for _ in range(0, 10)]:
    for t1, t2 in [(random.choice(range(0, len(ord_parts[0]))), random.choice(range(0, len(ord_parts[0])))) for _ in range(0, 10)]:
        op = random.choice(operations)
        _ = ord_parts
        thing = "int(_[%d][%d] %s _[%d][%d])" % (s1, t1, op, s2, t2)
        print "if", thing, "!=", str(eval(thing)), ":"
        print "\texit(-1)"
#print "\n\texit(-1)"
