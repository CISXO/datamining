# datamining
## Assignment 1, Frequent Pattern Mining by Apriori Algorithm

Purpose
Understanding of the concept of frequent item sets
Understanding of the Apriori algorithm
Practice of applying data mining techniques to real large-scale data

Description
We can discover frequent gene sets from input data of functional categories and annotating genes. A frequent gene set means a set of genes that work for the same cellular functions frequently. Implement the Apriori algorithm to read the data set provided and find frequent gene sets with minimum support of 3.5%. Your program will print the frequent gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent gene set at each line, for example, {'YAL005c', 'YBR044c'} 3.80% support.

Data Set
Yeast genes annotated to 216 different cellular functions are given in a tab-delimited text file. Each row contains a set of genes having a cellular function. The cellular function IDs are shown at the first column.
## Assignment 2, Frequent Closed Pattern Mining by Charm Algorithm

Purpose
Understanding of the concept of frequent closed itemsets
Understanding of the Charm algorithm
Practice of applying data mining techniques to real large-scale data

Description
We can discover frequent closed gene sets from input data of functional categories and annotating genes. A frequent closed gene set means a set of genes frequently occurring in the same cellular functions, which does not have any super-set with the same support. Implement the Charm algorithm to read the data set provided and find frequent closed gene sets with minimum support of 3.5%. Your program will print the frequent closed gene sets with size greater than or equal to 2 into an output file. It will show the support of each frequent closed gene set at each line, for example, {YAL005c, YBR044c} 3.8% support

Data Set
Use the same data set as Assignment 1.
