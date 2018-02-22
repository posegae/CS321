To run 10-fold evaluation for K Means Clustering, run

python3 KMeans.py

This will print out the overall precision, recall, and f1 for each of the folds,
and it will save plot images under the KMeansGraphs directory.
'KMeansClusters{}.jpg' where {} is some number is the clustering result from
the {}th fold.
overallDataDistribution.jpy is the graph showing the distribution of the three
labels in the corresponding space



To run 10-fold evaluation for Decision Trees, run

python3 decisionTree.py


This will print out the precision, recall, and f1 for each of the folds.
The individual class statistics as well as the aggregate are printed.
Further, at the end of the validation, Precision, recall, and f1 scores are
plotted against the majority class baseline inside the 'DecisionTreeGraphs'
directory.

The DecisionTreeGraphs directory will also contain the best trees from each of
the folds
