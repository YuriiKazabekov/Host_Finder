d = dict()
if 1 not in d:
    d[1] = list()

d[1].append(1)
d[1].append(2)
d[1].append(3)

if 2 not in d:
    d[2] = list()

d[2].append(1)
d[2].append(1)
d[2].append(1)

print(d[1])
print(d[2])
print(d)