import math
import time

import numpy as np
import datetime
import sys

def main():
    data = []
    with open("assignment3_input.txt", 'r') as file:
        for line in file:
            data.append(list(map(float, line.strip().split('\t'))))


    return data

def calculate_Medoids_first(datas):
    distance = np.array([])
    datas = np.array(datas)
    for data in datas:
        tmp = []
        for data1 in datas:
            if np.array_equal(data, data1, equal_nan=False):
                pass
            else:
                tmp.append(round(math.sqrt(np.sum(np.power(data1 - data, 2))),3))
        distance = np.append(distance, np.sum(np.array(tmp)))

    tmp1 = []
    tmp1.append(distance)
    tmp1= np.array(tmp1)
    tmp1.sort()

    Medoids = []
    for i in range (10):
        aindex = np.where(distance == tmp1[0][i])
        Medoids.append(datas[aindex[0][0]])


    return Medoids



def nearest_medoids(object, medoids):
    distances = []
    for medoid in medoids:
        distances.append(round(math.sqrt(np.sum(np.power(object-medoid, 2))), 3))
    return np.argmin(distances)


def calculate_Medoids(clusters):
    Medoids = []
    c_array = []
    for cluster in clusters :
        distance = np.array([])
        c_array = cluster
        c_array = np.array(c_array)
        for gene in c_array:
            tmp=[]
            for gene1 in c_array:
                if np.array_equal(gene, gene1, equal_nan=False):
                    pass
                else:
                    tmp.append(round(math.sqrt(np.sum(np.power(gene1 - gene, 2))), 3))
            distance = np.append(distance, np.sum(np.array(tmp)))
        min_index = np.argmin(distance)
        Medoids.append(c_array[min_index])

    return Medoids



start = time.time()
data = []
old_Medoids = []
if __name__ == '__main__':
    data = main()
Medoids = calculate_Medoids_first(data)

clusters = [[] for _ in range(10)]
for object in data:
    clusters[nearest_medoids(object, Medoids)].append(object)

while not(np.array_equal(old_Medoids, Medoids, equal_nan=False)):
    # compute the mean point of the objects in each cluster as a centroid
    old_Medoids = Medoids
    Medoids = calculate_Medoids(clusters)
    # assign each object to the nearest centroid and generate k new clusters

    clusters = [[] for _ in range(10)]
    for object in data:
        clusters[nearest_medoids(object, Medoids)].append(object)

end = time.time()
with open('./assignment3_output2.txt', 'w') as file:
    data
    for cluster in clusters:
        indexs = []
        for object in cluster:
            indexs.append(data.index(object))

        file.write(str(len(cluster)) + ': ' + " ".join(list(map(str, indexs))) + '\n')

    elapsed = end - start
    print(elapsed)