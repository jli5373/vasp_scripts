import sys
import numpy as np
from sklearn import linear_model 
from sklearn.linear_model import LinearRegression

correlation_matrix_file = sys.argv[1]
formation_energies_file = sys.argv[2]
testx_file = 'test_x.txt'
testy_file = 'test_y.txt'


x = np.loadtxt(correlation_matrix_file)
y = np.loadtxt(formation_energies_file)
testx = np.loadtxt(testx_file)
testy = np.loadtxt(testy_file)

reg = LinearRegression().fit(x,y)
print(reg.score(x,y))
print(reg.coef_)
print(reg.intercept_)
print(reg.predict(testx))
print(testy)


