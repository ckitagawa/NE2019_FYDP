import time
import numpy as np
import pickle
import os
from random import *
import matplotlib.pyplot as plt
%matplotlib inline

def gauss(x, y,x0,y0,sx,sy):
    #print((-(x-x0)**2/2/sx-(y-y0)**2/2/sy))
    return np.exp(-(x-x0)**2/2/sx-(y-y0)**2/2/sy)

x0=4.5
y0=4.5
sx=1
sy=1

if True:   
    #Generate Fake Data:
    n=10;
    frac1=0.25
    frac2=0.7
    frac3=0.1
    w=0;
    
    numsamples=10;
    
    ardata = [0.0] * 20
    linedata = [0.0] * 20*numsamples
    flush = False
    cnt = 0
    xs = [0.0] * 10
    ys = [0.0] * 10
    
    while True:
        
        x0=9*random()
        y0=9*random()
        sx=2*random()
        sy=2*random()
        
        #w+=2*random()-1
        w+=0.1
    
        M=np.ones((n,n))
 
        for i in range(0, n):
            for j in range(0, n):
                M[i][j]=gauss(i,j,x0,y0,sx,sy)+(2*random()-1)*frac1
            
        sumX=np.sum(M, axis=0)
        sumY=np.sum(M, axis=1)
        
        summat=np.ones((2*n))
    
        for i in range(0, n):
            summat[i]=sumX[i]+(2*random()-1)*frac2
        for i in range(0, n):
            summat[i+n]=sumY[i]+(2*random()-1)*frac2
        
        for ii in range(0, 2*n):
            if cnt == 0:
                ardata = [1.0] * 20
                linedata = [0.0] * 20*numsamples

            
            ardata[cnt] = summat[cnt]
            
            for i in range(0,numsamples):
                linedata[cnt*numsamples+i]=summat[cnt]+np.sin(i*w)*frac3*summat[cnt]
            
            cnt = (cnt + 1) % 20
            if cnt == 0:
                flush = True

            if flush:
                with open('tmp_ardata.pkl', 'wb') as output:
                    pickle.dump(ardata, output, pickle.HIGHEST_PROTOCOL)
                os.remove('ardata.pkl')
                os.rename('tmp_ardata.pkl', 'ardata.pkl')

                with open('tmp_linedata.pkl', 'wb') as output:
                    pickle.dump(linedata, output, pickle.HIGHEST_PROTOCOL)
                os.remove('linedata.pkl')
                os.rename('tmp_linedata.pkl', 'linedata.pkl')
                flush = False

        plt.imshow(M)  
        print([x0, y0, sx, sy, w])
        
        
        time.sleep(1)