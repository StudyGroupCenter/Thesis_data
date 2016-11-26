import matplotlib.pyplot as plt
import numpy as np
import math
import os

print os.getcwd()
#os.chdir(r'D:\Users\outao\Canopy_place')

plt.xlabel("Logarithm of reuse distance")
plt.ylabel("Logarithm of reuse distance frequency")
#plt.title("Distance among repeated submissions of the same query")
filename="reuse_frequency_aol"
sogoufile="reuse_frequency_sogou"
tf=open(filename)
x=[]
y=[]
x2=[]
y2=[]

line=tf.readline()
while line:
    rd=int(line.replace("\n","").split(" ")[0])#*3633623.0/11796397
    frequency=int(line.replace("\n","").split(" ")[1])#*11796397.0/3633623
    if frequency>1:
        logf=math.log(frequency,10)
        logrd=math.log(rd,10)
        x.append(logrd)
        y.append(logf)
    line=tf.readline()
tf.close()

sf=open(sogoufile)
line=sf.readline()

while line:
    rd=int(line.replace("\n","").split(" ")[0])#*3378504.0/14515148
    frequency=int(line.replace("\n","").split(" ")[1])#*14514148.0/3378504
    if frequency>1:
        logf=math.log(frequency,10)
        logrd=math.log(rd,10)
        x2.append(logrd)
        y2.append(logf)
    line=sf.readline()
sf.close()
plt.rcParams['font.family']="time-new-roman"
plt.rcParams['legend.frameon']=False
plt.rcParams['legend.handleheight']=0.1
plt.rcParams['legend.handletextpad']=0.1
plt.rcParams['legend.fontsize']=9.0
plt.rcParams['font.size']=9.0
plt.plot(x,y,'--',label="$company A$")
plt.plot(x2,y2,label="$company B$")
plt.legend()

plt.show()
