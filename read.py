import numpy as np
import random
import sys

test = np.loadtxt('test.csv', delimiter=',')
rnd = random.randrange(100)
rnd = rnd * 1/40

print(rnd)
