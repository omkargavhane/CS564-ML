import numpy as np
from pprint import pprint
import time
import math
#vectors=[[50, 11], [36, 9], [58, 20], [28, 20], [87, 85], [58, 1], [62, 79], [93, 4], [17, 76], [58, 87], [80, 96], [83, 37], [71, 74], [30, 84], [11, 50], [53, 41], [64, 9], [9, 77], [61, 85], [65, 2], [27, 86], [14, 72], [66, 86], [1, 43], [94, 98], [98, 34], [78, 89], [94, 67], [67, 35], [23, 84]]

v=[[2,4,5,6],[7,6,4,5],[9,6,2,3],[7,9,3,2]]
def minkowski_metric(v1,v2,p=2):
    '''Fucntion to calculate distance between two vectors depending on the given value of p'''
    if len(v1)==len(v2):
        sum=0
        for i in range(len(v1)):
            sum+=abs(v1[i]-v2[i])**p
        return sum**(1/p)

def calculate_centroid(cluster_members,center_update_metric):
    #take transpose such that it becomes easy to get features easily 
    cluster_members=np.array(cluster_members).T.tolist()
    if center_update_metric=='mean':
        centroid=list(map(lambda v:sum(v)/len(v),cluster_members))
    elif center_update_metric=='medoid':
        centroid=[]
        for col in cluster_members:
            col.sort()
            if len(col)%2==0:
                i=int(len(col)/2)
                j=int(i-1)
                centroid.append((col[i]+col[j])/2)
            else:
                i=int(math.floor(len(col)/2))
                centroid.append(col[i])
    return centroid
