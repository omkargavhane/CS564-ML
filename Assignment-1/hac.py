from essentials import *
from preprocessing import *

hac_distance_matrix=None
def find_closest_clusters():
    global hac_distance_matrix
    min_distance=hac_distance_matrix[1][0]
    min_distance_rno=1
    min_distance_cno=0
    for r_no in range(len(hac_distance_matrix)):
        for c_no in range(len(hac_distance_matrix)):
            if r_no>c_no and hac_distance_matrix[r_no][c_no]<min_distance:
                min_distance=hac_distance_matrix[r_no][c_no]
                min_distance_rno=r_no
                min_distance_cno=c_no
    return([min_distance_rno,min_distance_cno])

def distance_between_cluster(cno1,cno2,ci,linkage_method='single'):
    #print(cno1,cno2,ci)
    global hac_distance_matrix
    if cno1>ci:
        distance_cno1=hac_distance_matrix[cno1][ci]
    elif ci>cno1:
        distance_cno1=hac_distance_matrix[ci][cno1]
    if cno2>ci:
        distance_cno2=hac_distance_matrix[cno2][ci]
    elif ci>cno2:
        distance_cno2=hac_distance_matrix[ci][cno2]
    if linkage_method=='single':ret=min(distance_cno1,distance_cno2)
    elif linkage_method=='complete':ret=max(distance_cno1,distance_cno2)
    elif linkage_method=='average':ret=(distance_cno1+distance_cno2)/2
    return ret

def update_hac_distance_matrix(cno1,cno2,linkage_method):
    global hac_distance_matrix
    cluster_with_min_no=min(cno1,cno2)
    cluster_with_max_no=max(cno1,cno2)
    for ci in range(len(hac_distance_matrix)):
        if ci!=cno1 and ci!=cno2:
            distance_with_ci=distance_between_cluster(cno1,cno2,ci)
            if ci<cluster_with_min_no:
                hac_distance_matrix[cluster_with_min_no][ci]=distance_with_ci
            else:
                hac_distance_matrix[ci][cluster_with_min_no]=distance_with_ci
    hac_distance_matrix.pop(cluster_with_max_no)
    hac_distance_matrix_transpose=np.array(hac_distance_matrix).T.tolist()
    hac_distance_matrix_transpose.pop(cluster_with_max_no)
    hac_distance_matrix=np.array(hac_distance_matrix_transpose).T.tolist()



def initialize_hac_distance_matrix(vectors):
    global hac_distance_matrix
    no_of_vectors=len(vectors)
    row=[None for i in range(no_of_vectors)]
    hac_distance_matrix=[row.copy() for i in range(no_of_vectors)]
    for r_no in range(no_of_vectors):
        for c_no in range(no_of_vectors):
            if r_no>c_no:
                hac_distance_matrix[r_no][c_no]=minkowski_metric(vectors[r_no],vectors[c_no])

clusters={}
def hac(vectors,linkage_method='single'):
    global hac_distance_matrix
    initialize_hac_distance_matrix(vectors)
    '''
    hac_distance_matrix=[[None,None,None,None,None,None],
                         [0.71,None,None,None,None,None],
                         [5.66,4.95,None,None,None,None],
                         [3.61,2.92,2.24,None,None,None],
                         [4.24,3.54,1.41,1.00,None,None],
                         [3.20,2.50,2.50,0.50,1.12,None]]
    '''
    for i in range(len(hac_distance_matrix)-2):
        #pprint(hac_distance_matrix)
        #print(find_closest_clusters())
        cno1,cno2=find_closest_clusters()
        cluster_with_min_no=min(cno1,cno2)
        cluster_with_max_no=max(cno1,cno2)
        '''
        if cluster_with_min_no in clusters:
            clusters[cluster_with_min_no+i]=[clusters[cluster_with_min_no+i],cluster_with_max_no+i]
            print(clusters)
        else:
            clusters[cluster_with_min_no+i]=[cluster_with_min_no+i,cluster_with_max_no+i]
            print(clusters)
        '''
        #print(cno1,cno2)
        #clusters.append([[cno1+i,cno2+i],min(cno1,cno2)+i])
        update_hac_distance_matrix(cno1,cno2,linkage_method)
        print(i+1)

start=time.time()
header,vectors=estimate_missing_value("BR_mod.csv",'')
hac(vectors)
stop=time.time()
print('Time taken in seconds :',stop-start)

