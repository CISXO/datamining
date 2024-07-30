# datamining

## Assignment 3, Clustering by fast k-Medoids

Purpose
Understanding of the improved partition-based clustering algorithms such as k-medoids
Practice of applying clustering techniques to high-dimensional data

Description

It has been kept private due to copyright.

Fast k-Medoids Algorithm
Select initial medoids:
Calculate the distance between every pair of objects.
Calculate the sum of distance for each object.
Select k objects having the smallest sum of distance as initial medoids.
Obtain the initial clusters by assigning each non-medoid to the nearest medoid.
Update medoids iteratively:
For each cluster, calculate the sum of distance within the cluster for each object and select a new medoid having the smallest sum of distance.
Obtain the updated clusters by assigning each non-medoid to the nearest medoid.
Repeat steps 2-1 and 2-2 until the clusters do not change.
## Assignment 4, Clustering by k-Medoids

Purpose
Understanding of the improved partition-based clustering algorithms such as k-medoids
Practice of applying clustering techniques to high-dimensional data

Description

It has been kept private due to copyright.

k-Medoids Algorithm
Select initial medoids:
Select k objects randomly as initial medoids.
Obtain the initial clusters by assigning each non-medoid to the nearest medoid.
Update medoids iteratively:
Calculate the total cost (i.e., the sum of distance between each non-medoid and its nearest medoid).
For each non-medoid that is nearest from any medoid and has not been medoid previously, swap the non-medoid and it nearest medoid if the total cost decreases.
Repeat step 2-2 until the total cost does not decrease.
## Assignment 5, Cluster Validation
 

Purpose
Understanding of cluster validation methods

Description

It has been kept private due to copyright.

