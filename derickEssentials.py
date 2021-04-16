#!/Users/derickober/anaconda3/bin/python
import numpy as np

def columnSort(matrix, columnIndex):
    #sorts a matrix by the specified column
    #1st column (far left) is column 0

    columnIndex = int(columnIndex)
    sortedMatrix = matrix[np.argsort(matrix[:, columnIndex])]
    return sortedMatrix