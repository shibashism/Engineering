import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import sklearn
from sklearn import tree
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

data = pd.read_csv("cosmetics.csv")
print(data.head())

encoder = preprocessing.LabelEncoder()
data = data.apply(encoder.fit_transform)
print(data.head())

train, test = train_test_split(data, test_size=0.3, stratify=data['BUYS'])
train_X = train[train.columns[1:5]]
train_Y = train['BUYS']
test_X = test[test.columns[1:5]]
test_Y = test['BUYS']

dt_x = list()
dt_y = list()

best_depth = 0
best_acc = 0

for i in range(2, 11):
    dt = tree.DecisionTreeClassifier(max_depth=i, criterion='entropy')
    dt.fit(train_X, train_Y)
    predict = dt.predict(test_X)
    answer = sklearn.metrics.accuracy_score(test_Y, predict) * 100
    if answer > best_acc:
        best_acc = answer
        best_depth = i
    print('Accuracy of decision tree for max depth:', i, 'is:', answer, '%')
    dt_x.append(i)
    dt_y.append(answer)

plt.scatter(dt_x, dt_y)

plt.title('Decision tree variation of max depth vs accuracy')
plt.xlabel('Max depth of decision tree')
plt.ylabel('Accuracy of decision tree')
# plt.show()


print("Confusion Matrix :\n")
print(confusion_matrix(predict, test_Y, labels=[1, 0]))

dt = tree.DecisionTreeClassifier(max_depth=best_depth, criterion='entropy')
dt.fit(train_X, train_Y)

from sklearn import tree
import graphviz

dot_data = tree.export_graphviz(dt, out_file=None, feature_names=data.columns[1:-1])

graph = graphviz.Source(dot_data)
graph.render("dt")
