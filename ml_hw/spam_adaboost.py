import numpy as np
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold


def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    parser.add_argument('--numTrees', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def adaboost(X, y, num_iter):
    """Given an numpy matrix X, a array y and num_iter return trees and weights

    Input: X, y, num_iter
    Outputs: array of trees from DecisionTreeClassifier
             trees_weights (w) array of floats
    Assumes y is in {-1, 1}^n
    """
    trees = []
    w = [1 / float(len(y) + 1)] * len(y)
    alpha = []
    # your code here
    for m in range(num_iter):
        h = DecisionTreeClassifier(max_depth=1)
        tree = h.fit(X, y, sample_weight=w)
        pred = tree.predict(X)  # ?
        truth = 1 - (pred == y)
        num = np.dot(w, truth)
        error = num / np.sum(w)
        a = np.log((1 - error) / error)
        alpha.append(a)
        w = w * np.exp(a * truth)
        trees.append(tree)
    return trees, alpha


def adaboost_predict(X, trees, alpha):
    """Given X, trees and weights predict Y

    assume Y in {-1, 1}^n
    """
    tree2 = [trees[i].predict(X) for i in range(len(trees))]
    Yhat = np.dot(np.transpose(tree2), np.array(alpha))
    Yhat = np.sign(Yhat)
    return Yhat


def parse_spambase_data(filename):
    """ Given a filename return X and Y numpy arrays

    X is of size number of rows x num_features
    Y is an array of size the number of rows
    Y is the last element of each row.
    """
    f = pd.DataFrame.from_csv(filename, index_col=None, header=None)
    X = f.iloc[:, 0:-1].as_matrix()
    Y = f.iloc[:, -1].as_matrix()
    return X, Y


def new_label(Y):
    """ Transforms a vector od 0s and 1s in -1s and 1s.
    """
    return [-1. if y == 0. else 1. for y in Y]


def old_label(Y):
    return [0. if y == -1. else 1. for y in Y]


def accuracy(y, pred):
    return np.sum(y == pred) / float(len(y))


def main():
    """
    This code is called from the command line via

    python adaboost.py --train [path to filename] --test [path to filename] --numTrees
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    num_trees = int(args['numTrees'][0])
    print train_file, test_file, num_trees

    # your code here
    train_X, train_Y = parse_spambase_data(train_file)
    test_X, test_Y = parse_spambase_data(test_file)

    trees, alpha = adaboost(train_X, new_label(train_Y), num_trees)
    Yhat_train = old_label(adaboost_predict(train_X, trees, alpha))
    Yhat_test = old_label(adaboost_predict(test_X, trees, alpha))

    ## here print accuracy and write predictions to a file
    acc_test = accuracy(test_Y, Yhat_test)
    acc = accuracy(train_Y, Yhat_train)
    print("Train Accuracy %.4f" % acc)
    print("Test Accuracy %.4f" % acc_test)

    fin = np.c_[test_X, test_Y, Yhat_test]
    np.savetxt('predictions.txt', fin, fmt='%.2f', delimiter=',')


if __name__ == '__main__':
    main()