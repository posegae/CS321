import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.metrics import *
from sklearn.metrics import *
from subprocess import call
import graphviz
import os
def ten_fold_validation():
    if not os.path.exists('DecisionTreeGraphs'):
        os.makedirs('DecisionTreeGraphs')

    df = pd.read_csv('HW3_Data.txt', delimiter='\t')

    # shuffle the data before running 10-fold cross validation
    df = df.sample(frac=1).reset_index(drop=True)

    # Encoding for non-numeric values
    df['Location Type'] = df['Location Type'].map({'Office': 0, 'Warehouse': 1})

    test_size = 400
    start = 0


    f1Stats = []
    precisionStats = []
    recallStats = []
    bestF1 = 0

    for i in range(10):
        test = df[start:start+test_size]
        train = df[~df['HeatMiser_ID'].isin(test['HeatMiser_ID'])].dropna()
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(train[['Distance_Feature', 'Speeding_Feature', 'Location Type']], train['OSHA'])

        results = clf.predict(test[['Distance_Feature', 'Speeding_Feature', 'Location Type']])
        actual = test['OSHA']
        tups = zip(results, actual)
        right = 0
        for tup in tups:
            if tup[0] == tup[1]:
                right += 1


        c_mat = confusion_matrix(actual, results, labels=['Safe', 'Compliant', 'NonCompliant'])

        print("\n\nTotal scores")
        precisionScore = precision_score(actual, results, average='weighted', labels=['Safe', 'Compliant', 'NonCompliant'])
        recallScore = recall_score(actual, results, average='weighted', labels=['Safe', 'Compliant', 'NonCompliant'])
        f1Score = f1_score(actual, results, average='weighted', labels=['Safe', 'Compliant', 'NonCompliant'])
        print("Precision / Recall / F1: {} / {} / {}".format(precisionScore, recallScore, f1Score))

        f1Stats.append(f1Score)
        precisionStats.append(precisionScore)
        recallStats.append(recallScore)

        print("\nClass scores")
        for label in ['Safe', 'Compliant', 'NonCompliant']:
            print("{}:".format(label))
            recisionScore = precision_score(actual, results, average='weighted', labels=[label])
            recallScore = recall_score(actual, results, average='weighted', labels=[label])
            f1Score = f1_score(actual, results, average='weighted', labels=[label])
            print("Precision / Recall / F1: {} / {} / {}".format(precisionScore, recallScore, f1Score))

        if bestF1 < f1Score:
            bestF1 = f1Score
            bestTree = clf

        start += test_size

        df_features = df.drop("OSHA", axis=1)
        dot_data = tree.export_graphviz(bestTree, out_file="tree.dot",
                                        feature_names=['Distance_Feature', 'Speeding_Feature', 'Location Type'],
                                        class_names=['Safe', 'Compliant', 'NonCompliant'],
                                        filled=True,
                                        special_characters=True)

        call(['dot', '-T', 'png', 'tree.dot', '-o', 'DecisionTreeGraphs/tree{}.png'.format(i + 1)])
        os.remove('tree.dot')
        # os.remove('DecisionTree')

    import matplotlib.pyplot as plt

    majorityTruePositive = df[df['OSHA'] == 'Safe'].shape[0]
    majorityFalsePositive = df.shape[0] - majorityTruePositive
    majorityPrecision = majorityTruePositive / (majorityTruePositive + majorityFalsePositive)
    majorityRecall = 1
    majorityF1 = 2 * ((majorityPrecision * majorityRecall) / (majorityPrecision + majorityRecall))

    print('Aggregate performance across all folds')
    print('Precision: {}'.format(sum(precisionStats) / len(precisionStats)))
    print('Recall: {}'.format(sum(recallStats) / len(recallStats)))
    print('F1: {}'.format(sum(f1Stats) / len(f1Stats)))


    plt.plot(range(1, 11), f1Stats)
    plt.plot(range(1, 11), [majorityF1] * 10)
    plt.ylim([0,1])
    plt.title('Decision Tree and Majority Baseline F1')
    plt.xlabel('Folds')
    plt.ylabel('F1')
    plt.savefig('DecisionTreeGraphs/F1Graph.jpg')

    plt.clf()
    plt.plot(range(1, 11), precisionStats)
    plt.plot(range(1, 11), [majorityPrecision] * 10)
    plt.ylim([0,1])
    plt.title('Decision Tree and Majority Baseline Precision')
    plt.xlabel('Folds')
    plt.ylabel('Recall')
    plt.savefig('DecisionTreeGraphs/PrecisionGraph.jpg')

    plt.clf()
    plt.plot(range(1, 11), recallStats)
    plt.plot(range(1, 11), [majorityRecall] * 10)
    plt.ylim([0,1.1])
    plt.title('Decision Tree and Majority Baseline Recall')
    plt.xlabel('Folds')
    plt.ylabel('Recall')
    plt.savefig('DecisionTreeGraphs/RecallGraph.jpg')

ten_fold_validation()
