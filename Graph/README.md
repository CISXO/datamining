# datamining
## Assignment 6, Graph Clustering by Top-Down Hierarchical Algorithm

Purpose
Understanding of hierarchical graph clustering algorithms
Practice of applying graph clustering techniques to large-scale graph data

Description

It has been kept private due to copyright.

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

It has been kept private due to copyright.

Bottom-Up Hierarchical Graph Clustering
Make each vertex of the graph become a single cluster
Repeat until all vertices of the graph are included into one cluster
List all edges between two vertices belonging to different clusters
Merge the two clusters that include the two vertices with the highest Jaccard index of the sets of their neighbors, which is greater than 0.1
If the merged cluster meets the density threshold, make it as a candidate cluster
In the set of candidate clusters, return only the maximal-sized supersets as the final clusters
