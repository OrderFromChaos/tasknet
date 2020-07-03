from collections import OrderedDict

d = OrderedDict()
d[1] = 1
d[2] = 2
d[3] = 3
print(d)
d[4] = 4
print(d)
d[1] = 5
print(d)

# OrderedDicts preserve original insertion order, not update order