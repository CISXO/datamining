# datamining
## Assignment 6, Graph Clustering by Top-Down Hierarchical Algorithm

Purpose
Understanding of hierarchical graph clustering algorithms
Practice of applying graph clustering techniques to large-scale graph data

Description
Genetic interaction data are provided to discover gene sets densely connected each other. The densely connected genes are likely to have the same cellular functions. Implement the top-down hierarchical graph clustering algorithm by least common neighbors using a density threshold of 0.4. Your python code should take an input file name as a command-line argument, and return an output file ("assignment6_output.txt") including the gene clusters of size-10 or greater. In an output file, show each cluster at each line in the format of the size and gene names in the cluster, for example, "4: YBR160W YDR224C YPL231W YBR081C". Print the clusters in a decreasing order of their size.

Top-Down Hierarchical Graph Clustering
Repeatedly remove an edge whose two ending vertices have the smallest Jaccard index of the sets of their neighbors until the graph is disconnected.
If the graph is disconnected into two sub-graphs:
If each sub-graph meets the density threshold, return the sub-graph as a cluster.
Otherwise, apply steps 1 and 2 to the sub-graph recursively until all vertices are returned as cluster members.

## Assignment 7, Graph Clustering by Bottom-Up Hierarchical Algorithm

Purpose
Understanding of hierarchical graph clustering algorithms
Practice of applying graph clustering techniques to large-scale graph data

Description
Genetic interaction data are provided to discover gene sets densely connected each other. The densely connected genes are likely to have the same cellular functions. Implement the bottom-up hierarchical graph clustering algorithm by most common neighbors using a density threshold of 0.4. Your python code should take an input file name as a command-line argument, and return an output file ("assignment7_output.txt") including the gene clusters of size-10 or greater. In an output file, show each cluster at each line in the format of the size and gene names in the cluster, for example, "4: YBR160W YDR224C YPL231W YBR081C". Print the clusters in a decreasing order of their size.

Bottom-Up Hierarchical Graph Clustering
Make each vertex of the graph become a single cluster
Repeat until all vertices of the graph are included into one cluster
List all edges between two vertices belonging to different clusters
Merge the two clusters that include the two vertices with the highest Jaccard index of the sets of their neighbors, which is greater than 0.1
If the merged cluster meets the density threshold, make it as a candidate cluster
In the set of candidate clusters, return only the maximal-sized supersets as the final clusters