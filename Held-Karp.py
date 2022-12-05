from cmath import inf
from dis import dis
import math
import random
import sys
from itertools import combinations
import time
import matplotlib
import matplotlib.pyplot as plt
import psutil
random.seed(0)
n =int(sys.argv[1])
    
print('Genero %s punti'%n)
#Create random adjacency matrix

dists=[]
P_x=[]
P_y=[]
for i in range(n):
    dists.append([0] * n)
    P_x.append(random.randint(-50, 50))
    P_y.append(random.randint(-50, 50))



for i in range(n):
    for j in range(i+1, n):
        dists[i][j] = dists[j][i] = math.sqrt((P_x[i]-P_x[j])**2+(P_y[i]-P_y[j])**2)
#End generation



time_start=time.perf_counter()
prima=psutil.virtual_memory()[3]

#Begin algorithm
Costs={}
for i in range(1, n):
    Costs[(1 << i, i)] = (dists[0][i], 0)

#Begin loops

for i in range(2,n): #Iteration on increasing subset
    for comb in combinations(range(1,n), i):   #Iteration on combinations of dimension i, N_c=N!/(i!*(N-i)!). Total complexity 2^n
        visits=0
        for k in comb:
            visits |= 1<<k #Setting 1 on bits representing visited cities.

        for k in comb: #Looking for shortest path through these cities. 
            prev = visits & ~(1<<k) #Marking visited cities. 
            best=inf
            last=0
            new=0

            for j in comb:
                if j==0 or j==k:
                    continue
                new=Costs[(prev, j)][0]+dists[j][k]
                if new<best:
                    best=new
                    last=j
            
            Costs[(visits,k)] = (best,last)

#Return home

visits=(2**n-1)-1 #Turn on all bits but the first
best=inf
last=0
new=0
for i in range(1, n):
    new=Costs[(visits, i)][0]+dists[i][0]
    if new<best:
        best=new
        last=i
Costs[(2**n-1, 0)]=(best,last)

#Extract best path
dopo=psutil.virtual_memory()[3]
print(dopo-prima)
next=(2**n-1, 0)
path=[0]
for i in range(0,n):
    path.append(Costs[next][1])
    next=(next[0]& ~(1<<next[1]), Costs[next][1])
    
path.reverse() #Reversing!

print(path)
time_end=time.perf_counter()

out=open('Memory.dat','a')
out.write('%d %f \n'%(n, dopo-prima))
'''
#-----------------Draw------------------------
X_ord=[]
Y_ord=[]
for i in path:
    X_ord.append(P_x[i])
    Y_ord.append(P_y[i])



print('\n')      

for i in range(n):
    for j in range(n):
        print('%.2f'%dists[i][j], end='\t')  
    print('\n')      



fig=plt.figure(figsize=(8, 8))
#plt.plot(X_ord, Y_ord, marker='o',)
plt.plot(X_ord, Y_ord, marker='o', linewidth=1)
for i, txt in enumerate(path):
    plt.annotate(txt, (X_ord[i], Y_ord[i]),xytext=(X_ord[i]+0.5, Y_ord[i]+0.5))

#plt.show()

'''