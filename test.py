import numpy as np

matrix = np.ones((3, 5))
matrix[2, 2] = 2
array = np.array([1, 2, 3])

print(matrix)
print(matrix.swapaxes(1,0))
print(array)
print(matrix.swapaxes(1,0).dot(array))
print(matrix)