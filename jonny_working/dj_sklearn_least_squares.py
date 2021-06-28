#Put this all into a Jupyter notebook

import sys
import numpy as np
from sklearn import linear_model 
from sklearn.linear_model import LinearRegression

#do we want basis.json?
#can probably pull all this from JSONs
#avoid sys.argv, use argparse instead (although thats not really necessary for the Jupyter notebook)
correlation_matrix_file = sys.argv[1] #output of "casm query -k 'corr' -o outputfile.txt"
formation_energies_file = sys.argv[2] #output of "casm query -k 'formation_energy' -o outputfile_energy.txt"
#filenames
#add object to figure out which ECIs you want selected
#ex. ECI_on = [1 2 3 4 5]
#have something to pick which corr's to turn on
#easier to load JSON data in instead

#testx_file = 'test_x.txt'
#testy_file = 'test_y.txt'


x_raw = np.genfromtxt(correlation_matrix_file, skip_header=1) #rows are SCELs columns are each correlation function
y_raw = np.genfromtxt(formation_energies_file, skip_header=1) #a row of energies
x = x_raw[:,2:-1]
y = y_raw[:,2]
#print(x)
#print(y)

#split randomly (realized the scikitlearn can do this already)\
#make kfolds variable
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
    print("Score:")
    print(reg.score(x,y))
    print("ECIs:")
    print(reg.coef_) #these ECIs 
    print("Intercept")
    print(reg.intercept_)
    print("Prediction:")
    print(reg.predict(testx))
    print("Actual Energies")
    print(testy)
    print("Difference")
    print(testy-reg.predict(testx))
    print('-------------------')
    #Can output it to files instead
    #Can plot predicted vs calculated
    #Generate convext hull (probably easy python method)