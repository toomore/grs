from time import time
from datetime import datetime
from grs import stock
t = time()
a = []
times = 1

for i in range(times):
    tt = time()
    stock(1201).MA(3)
    a.append(time()-tt)

print "end {0}".format(datetime.now())
print "Max: {0}".format(max(a))
print "Min: {0}".format(min(a))
print "ALL: {0}".format(time()-t)
print "Avg: {0}".format((sum(a)-max(a)-min(a))/(times-2))
