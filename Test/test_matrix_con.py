'''
Test matrix conventions
'''
import numpy as np

M = np.zeros((4,5))
M[:,] = np.linspace(40, 60, 5)
M[, :] = np.linspace(-6, 8, 4)


print M
