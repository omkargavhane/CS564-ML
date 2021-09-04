from essentials import *
from preprocessing import *
import random
from pprint import pprint
import matplotlib.pyplot as plt


clusters={}
centroids=[]
#used sklearn and numpy only to predict the missing values

def initialize_clusters(vectors,k):
    global clusters,centroids
    clusters={}
    centroids=[]
    centroids=random.sample(vectors,k)
    for i in range(k):
        clusters[i]={'centroid':centroids[i],'members':[],'members_dist':[]}

def remove_vector_from_cluster(current_cluster_no,vector,center_update_metric):
    global clusters,centroids
    index_of_vector_in_current_cluster=clusters[current_cluster_no]['members'].index(vector)
    clusters[current_cluster_no]['members'].pop(index_of_vector_in_current_cluster)
    clusters[current_cluster_no]['members_dist'].pop(index_of_vector_in_current_cluster)
    clusters[current_cluster_no]['centroid']=calculate_centroid(clusters[current_cluster_no]['members'],center_update_metric)
    centroids[current_cluster_no]=copy.deepcopy(clusters[current_cluster_no]['centroid'])

def add_vector_into_cluster(new_cluster_no,vector,distance,center_update_metric):
    global clusters,centroids
    clusters[new_cluster_no]['members_dist'].append(distance)
    clusters[new_cluster_no]['members'].append(vector)
    clusters[new_cluster_no]['centroid']=calculate_centroid(clusters[new_cluster_no]['members'],center_update_metric)
    centroids[new_cluster_no]=copy.deepcopy(clusters[new_cluster_no]['centroid'])

def update_clusters(current_cluster_no,new_cluster_no,vector,distance,center_update_metric):
    global clusters
    if current_cluster_no==None:
        add_vector_into_cluster(new_cluster_no,vector,distance,center_update_metric)
    elif current_cluster_no!=new_cluster_no:
        remove_vector_from_cluster(current_cluster_no,vector,center_update_metric)
        add_vector_into_cluster(new_cluster_no,vector,distance,center_update_metric)

def find_current_cluster_no_for_vector(vector):
    global clusters
    current_cluster_no=None
    for cno,cluster in clusters.items():
        if vector in cluster['members']:
            current_cluster_no=cno
    return current_cluster_no

def is_two_vectors_equal(vect1,vect2):
    if len(vect1)==len(vect2):
        if sum([1 if e in vect2 else 0 for e in vect1])==len(vect1):
            print("centroid matches with previous state")
            return True
    else:
        return False

def wcss():
    global clusters,centroids
    avg_wcss=0
    for cluster in clusters.values():
        avg_wcss+=sum(cluster['members_dist'])
    return avg_wcss

def kmean(vectors,k,center_update_metric,no_of_iterations=100):
    global clusters,centroids
    noi=0
    initialize_clusters(vectors,k)
    status_of_while_break=''
    while True:
        prev_clusters_centroid=copy.deepcopy(centroids)
        for vector in vectors:
            distances=[minkowski_metric(centroid,vector) for centroid in centroids]
            min_dist=min(distances)
            new_cluster_no=distances.index(min_dist)
            update_clusters(find_current_cluster_no_for_vector(vector),new_cluster_no,vector,min_dist,center_update_metric)
        noi+=1
        print(noi)
        if is_two_vectors_equal(prev_clusters_centroid,centroids) or noi==no_of_iterations:
            break 
    return prev_clusters_centroid

def elbow(vectors,k):
    avg_wcss_wrt_k=[]
    for i in range(1,k+1):
        kmean(vectors,i)
        avg_wcss_wrt_k.append(wcss())
    plt.scatter(x=range(1,k+1),y=avg_wcss_wrt_k)
    plt.show()
inpt=input("Mean or Medoid [n/d]:").lower()
start=time.time()
header,vectors=estimate_missing_value("BR_mod.csv",'')
if inpt=='n':
    #elbow(vectors,15,)
    pcc=kmean(vectors,5,'mean')
elif inpt=='d':
    #elbow(vectors,15,)
    pcc=kmean(vectors,5,'medoid')
stop=time.time()
print('Time taken in seconds :',stop-start)
