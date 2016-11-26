import matplotlib.pyplot as plt
import numpy as np
import math
import os

print os.getcwd()
#os.chdir(r'D:\Users\outao\Canopy_place')

plt.xlabel("Logarithm of popularity rank")
plt.ylabel("Logarithm of occurrences")
#plt.title("Occurrences of the queries")
filename="aol_rank"
sogoufile="sogou_rank"

tf=open(filename)
x=[]
y=[]
x2=[]
y2=[]

line=tf.readline()
rank = 0
while line:
    frequency=int(line.replace("\n","").split(" ")[0])
    rank += 1
    x.append(math.log(rank,10))
    y.append(math.log(frequency,10))
    line=tf.readline()
tf.close()

sf=open(sogoufile)
line=sf.readline()
rank = 0
while line:
    frequency=int(line.replace("\n","").split(" ")[0])
    rank += 1
    x2.append(math.log(rank,10))
    y2.append(math.log(frequency,10))
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
