l=[1,2,3,4]
q=[5,6,7,8]

x = l.index(2)
y = q.index(5)

l[y], l[x] = l[x], l[y]


print(l)
print(q)
