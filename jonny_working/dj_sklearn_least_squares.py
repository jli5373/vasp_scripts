import sys
import numpy as np
from sklearn import linear_model 
from sklearn.linear_model import LinearRegression

correlation_matrix_file = sys.argv[1] #output of "casm query -k 'corr' -o outputfile.txt"
formation_energies_file = sys.argv[2] #output of "casm query -k 'formation_energy' -o outputfile_energy.txt"

#testx_file = 'test_x.txt'
#testy_file = 'test_y.txt'


x_raw = np.genfromtxt(correlation_matrix_file, skip_header=1)
y_raw = np.genfromtxt(formation_energies_file, skip_header=1)
x = x_raw[:,2:-1]
y = y_raw[:,2]
print(x)
print(y)

for iter in range(0,10):
    print(iter)
    trainx = x[0:2,:]
    trainy = y[0:1]
    index = 0
    for i in x:
        if(index % 10 != iter):
            #print('----------\n')
            #print(trainx)
            #print('----------\n')
            #print(x[index])
            #print('----------\n')
            trainx=np.vstack((trainx,x[index]))
            trainy=np.append(trainy,y[index])
        index+=1
#    print(trainx)
#    print(trainy)
#    print('----------\n')
    trainx=np.delete(trainx,0,0)
    trainx=np.delete(trainx,0,0)
    trainy=np.delete(trainy,0)
    #print(trainx)
    #print(trainy)
    #print('end-------------\n')

    testx = x[iter::10,:]
    testy = y[iter::10]
    reg = LinearRegression().fit(x,y)
    print(reg.score(x,y))
    print(reg.coef_)
    print(reg.intercept_)
    print(reg.predict(testx))
    print(testy)
    print('-------------------')