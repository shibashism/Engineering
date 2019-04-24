import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

data = pd.read_csv("dataset.csv")
# print(data.head())

x = data.iloc[:,:-1]
print(x)

y = data.iloc[:,5].values
print(y)

from sklearn.preprocessing import LabelEncoder

x = x.apply(LabelEncoder().fit_transform)
print(x)

from sklearn.tree import DecisionTreeClassifier

regressor = DecisionTreeClassifier(criterion='entropy')

regressor.fit(x.iloc[:,1:5],y)

x_in = [1,1,0,0]
y_predict = regressor.predict([x_in])

print(y_predict)


from IPython.display import Image
from sklearn.externals.six import StringIO
from sklearn.tree import export_graphviz
import pydotplus


dot_point =  StringIO()
export_graphviz(regressor,out_file=dot_point,rounded='True',filled='True',special_characters='True',
                feature_names=['Age','Income','Gender','Marital status'])
graph = pydotplus.graph_from_dot_data(dot_point.getvalue())
graph.write_png("DataGraph.png")