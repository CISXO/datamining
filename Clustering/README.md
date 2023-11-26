# datamining

## Assignment 3, Clustering by fast k-Medoids

Purpose
Understanding of the improved partition-based clustering algorithms such as k-medoids
Practice of applying clustering techniques to high-dimensional data

Description
A time-series gene expression data set is provided to discover gene sets with co-expression patterns (similar expressions during a given time range). The co-expressed genes are likely to have the same cellular functions. Implement improved k-Medoids (described below) with k=10 to find 10 clusters of genes. Use Euclidean distance to measure distance between data objects. Your python code should take an input file name as a command-line argument, and return an output file named "assignment3_output.txt". In an output file, show the gene IDs of each cluster at each line (space-delimited) starting with the size of the cluster. For example, "6: 0 24 56 139 285 471" where '6' is the cluster size and "0 24 56 139 285 471" are the six gene IDs in the cluster. Print the elapsed time of your python script in microseconds to the screen.

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
A time-series gene expression data set is provided to discover gene sets with co-expression patterns (similar expressions during a given time range). The co-expressed genes are likely to have the same cellular functions. Implement k-Medoids (described below) with k=10 to find 10 clusters of genes. Use Euclidean distance to measure distance between data objects. Your python code should take an input file name as a command-line argument, and return an output file named "assignment4_output.txt". In an output file, show the gene IDs of each cluster at each line (space-delimited) starting with the size of the cluster. For example, "6: 0 24 56 139 285 471" where '6' is the cluster size and "0 24 56 139 285 471" are the six gene IDs in the cluster. Print the elapsed time of your python script in microseconds to the screen.

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
Cluster validation is the process of assessing quality of clustering results. Clustering results are validated to compare the performance of clustering algorithms. Implement two cluster validation methods: (1) the use of incident matrices, and (2) the f-measure. Your python codes should take two input file names as command-line arguments, (1) a file of clustering results from Assignment-3 OR Assignment-4, and (2) a file of the ground-truth dataset provided below. To use incident matrices, apply the Jaccard index of the entry values between two incident matrices, and print the Jaccard index to the screen. To use the f-measure, find the highest f-score among the ground-truth clusters for each output cluster, and print the average of the highest f-scores of all output clusters to the screen. Also, print the elapsed time of your python codes in microseconds to the screen

