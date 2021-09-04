import arff,copy
from sklearn import preprocessing
import numpy as np
#{0:'core',1:'outlier',2:'boundary'}

def minkowski_metric(v1,v2,p=1):
    '''Fucntion to calculate distance between two vectors depending on the given value of p'''
    if len(v1)==len(v2):
        sum=0
        for i in range(len(v1)):
            sum+=abs(v1[i]-v2[i])**p
        return sum**(1/p)


class dbscan:
    def __init__(self,fname,eps,minpts):
        self.eps=eps
        self.minpts=minpts
        self.vectors=None
        self.distances=None
        self.clusters={}
        self.points={}
        self.cp=[]
        self.bp=[]
        self.op=[]
        self._read_file(fname)
        self._normalize()

    def _normalize(self):
        scaler = preprocessing.MinMaxScaler(feature_range=(0,5))
        self.vectors=scaler.fit_transform(np.array(self.vectors).T).T.tolist()

    def _read_file(self,fname):
        #read file.drop last elements of each row  i.e test result
        self.vectors=[e._values[:-1] for e in arff.load(fname)]

    def calculate_distance(self):
        #create a empty list wherer all elements initialized with 0
        row=[0 for i in range(len(self.vectors))]
        #create distances matrix 
        self.distances=[copy.deepcopy(row) for i in range(len(self.vectors))]
        #calculates teh distance between two points
        for r in range(len(self.distances)):
            for c in range(len(self.distances)):
                self.distances[r][c]=minkowski_metric(self.vectors[r],self.vectors[c])
                self.distances[c][r]=self.distances[r][c]

    def classify_points(self):
        #first finds core and outlier points
        for r in range(len(self.distances)):
            #get all memebers within the radius of current points 
            members=[[i,self.distances[r][i]] for i in range(len(self.distances[r])) if self.distances[r][i]<=self.eps]
            if len(members)>=self.minpts: #if no of members is >= minpts then make point as core 
                self.points[r]={'point':0,'members':members}
            else:  #else make it as outlier
                self.points[r]={'point':1,'members':members}
        #loop to seperate the boundary point from outlier
        for cno,cinfo in self.points.items():
            if cinfo['point']==1: #check whether it is outlier
                for member in cinfo['members']: #get all the points in clusters
                    if self.points[member[0]]['point']==0: #if any core point found
                        self.points[cno]['point']=2 #make current point as boundary point
        self._points_summary()

    def _points_summary(self):
        print("[ Data point summary ]")
        self.cp=[];self.bp=[];self.op=[]
        for cno,cinfo in self.points.items():
            if cinfo['point']==0:self.cp.append(cno)
            elif cinfo['point']==1:self.op.append(cno)
            elif cinfo['point']==2:self.bp.append(cno)
        print('[No of Points]','Core:',len(self.cp),'Boundary:',len(self.bp),'Outlier:',len(self.op))

    def _ismember_cluster(self,cp):
        for members in self.clusters.values():
            if cp in members:
                return True
        return False

    def find_clusters(self):
        for cp in self.cp:
            if not self._ismember_cluster(cp):
                temp=[cp]
                self.clusters[cp]=[]
                while temp:
                    t=[member[0]  for member in self.points[temp[0]]['members'] if member[0] not in self.op and not self._ismember_cluster(member[0])]
                    temp.extend(t)
                    self.clusters[cp].extend(t)
                    temp.pop(0)
        obj._cluster_summary()

    def _cluster_summary(self):
        print("[ Cluster summary ]")
        print("No of clusters:",len(self.clusters.keys()))
        cno=self.clusters.keys()
        for e in cno:
            print("Clusters no:",e,"No of members:",len(self.clusters[e]))
        for cno,members in self.clusters.items():
            print()
            print("cluster no:",cno,members)


obj=dbscan('diabetes1.arff',2,5)
obj.calculate_distance()
obj.classify_points()
obj.find_clusters()
