import numpy as np
import argparse
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold

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

def accuracy(y, pred):
    return np.sum(y == pred) / float(len(y))

train_X, train_Y = parse_spambase_data('spambase.train')
test_X, test_Y = parse_spambase_data('spambase.test')

clf = GradientBoostingClassifier(loss='deviance', learning_rate=0.1,
                             n_estimators=500, subsample=0.3,
                             min_samples_split=2,
                             min_samples_leaf=1,
                             max_depth=1,
                             random_state=None,
                             max_features=None,
                             verbose=2)
clf.fit(train_X, train_Y)
Yhat_train = clf.predict(train_X)
Yhat_test = clf.predict(test_X)

acc_test = accuracy(test_Y, Yhat_test)
acc = accuracy(train_Y, Yhat_train)
print("Train Accuracy %.4f" % acc)
print("Test Accuracy %.4f" % acc_test)

n = [10, 25, 50, 100, 200, 300, 400, 500]
trainE = [0.9111, 0.9256, 0.9325, 0.9408, 0.9447, 0.9475, 0.9492, 0.9494]
validE = [0.9190, 0.9350, 0.9440, 0.9470, 0.9510, 0.9490, 0.9500, 0.9530]
GBtrainE = [0.9169, 0.9314, 0.9464, 0.9583, 0.9717, 0.9747, 0.9869, 0.9914]
GBtestE = [0.9350, 0.9360, 0.9470, 0.9490, 0.9550, 0.9500, 0.9610, 0.9610]
line_up, = plt.plot(n, GBtrainE, label='Training')
line_down, = plt.plot(n, GBtestE, label='Testing')
plt.legend(handles=[line_up, line_down])
plt.title('Accuracy scores for gradient boosting')
plt.xlabel("# of estimators")
plt.ylabel("Accuracy")
plt.show()