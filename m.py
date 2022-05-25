import sys
import numba
import numpy

print("Python version:", sys.version)
print("Numba version:", numba.__version__)
print("Numpy version:", numpy.__version__)

from numba import cuda
import numpy as np

@cuda.jit
def cudakernel0(array):
    for i in range(array.size):
        array[i] += 0.5

array = np.array([0, 1], np.float32)
print('Initial array:', array)

print('Kernel launch: cudakernel0[1, 1](array)')
cudakernel0[1, 1](array)

print('Updated array:',array)

