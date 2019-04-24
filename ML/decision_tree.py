import pandas as pd  #
from sklearn.tree import DecisionTreeClassifier  #
from sklearn import preprocessing  #
from sklearn import tree  #
import graphviz  #
from sklearn.model_selection import train_test_split  #
from sklearn.metrics import accuracy_score  #
from sklearn.metrics import classification_report  #
from sklearn.metrics import confusion_matrix  #
import os

# os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin\\'

data = pd.read_csv("as2.csv")

print("data type od data : ", type(data))
features = data.columns
print("Features :", features)
features = features[1:-1]
print("Features after pruning :", features)
class_names = list(set(data.iloc[:, -1]))
print("Class names :", class_names)

# Label encode data
print("data.columns.values : ", data.columns.values)
lencoder = preprocessing.LabelEncoder()
for i in data.columns.values:
    if data[i].dtype == "object":
        data[i] = lencoder.fit_transform(data[i])


# split data into train test split

# X = data[['Age', 'Income', 'Gender', 'Marital Status']]
X = data.iloc[:, 1:-1]
print("Data :", X)
Y = data['Buys']
print("Classes ", Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
print("X_train :", X_train)
print("y_train :", y_train)
print("X_test :", X_test)
print("Y_test :", y_test)

# decision tree using gini index

modelgini = DecisionTreeClassifier(criterion="entropy")
modelgini.fit(X_train, y_train)
y_pred = modelgini.predict(X_test)

print("Predications :", y_pred)

print("Confusion Matrix: ",
      confusion_matrix(y_test, y_pred))

print("Accuracy : ",
      accuracy_score(y_test, y_pred) * 100)

print("Report : ",
      classification_report(y_test, y_pred))

print(features)
print(class_names)

plottree = tree.export_graphviz(modelgini, out_file=None, feature_names=features, class_names=class_names, filled=True,
                                rounded=True, special_characters=True)
graph = graphviz.Source(plottree)
graph.render('DecisionTree3', view=True)

from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
# from IPython.Display import Image
import pydotplus

dot_data = StringIO()

export_graphviz(modelgini, out_file=dot_data, feature_names=features, class_names=class_names, filled=True,
                rounded=True, special_characters=True)

# create the graph
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png('tree.png')
