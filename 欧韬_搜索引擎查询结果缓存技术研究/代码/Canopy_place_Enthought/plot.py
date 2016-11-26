import matplotlib.pyplot as plt
import numpy as np
import math
import os

print os.getcwd()
#os.chdir(r'D:\Users\outao\Canopy_place')

plt.xlabel("logarithm of Reuse Distance")
plt.ylabel("logarithm of Reuse Distance Frequency")
filename="reuse_frequency_sogou"


tf=open(filename)
x=[]
y=[]

line=tf.readline()
while line:
    rd=int(line.replace("\n","").split(" ")[0])
    frequency=int(line.replace("\n","").split(" ")[1])
    if frequency>1:
        logf=math.log(frequency,10)
        logrd=math.log(rd,10)
        x.append(logrd)
        y.append(logf)
    line=tf.readline()

plt.plot(x,y,'*')

plt.plot(1,1)
tf.close()
plt.show()
