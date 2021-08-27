#importing numpy to use NaN and sklearn for predicting the missing values in dataset
import csv
import numpy as np
from sklearn.impute import KNNImputer
import copy

original_vectors=[]
def estimate_missing_value(file_name,estimate_for):
    global original_vectors
    '''Fumction to estimate the missing values in dataset using KNN method.returns the header and data with missing values predicted'''
    #Open csv file to read data
    with open(file_name) as f:
        vectors = list(csv.reader(f))
    original_vectors=copy.deepcopy(vectors[1:])
    #Iterate over all vectors if value for which we need to estimate is found replace it with NaN else convert to numeric
    temp=[]
    header=vectors[0]
    for vector in vectors[1:]:
        temp.append([np.nan if e==estimate_for else eval(e) for e in vector])
    #use of KNN from sklearn to estimate the missing values 
    imputer = KNNImputer(n_neighbors=5, weights="uniform")
    vectors=imputer.fit_transform(temp).tolist()
    return(header,vectors)

if __name__=='__main__':
    header,vectors=estimate_missing_value("BR_mod.csv",'')
