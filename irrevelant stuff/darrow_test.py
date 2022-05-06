# https://www.analyticssteps.com/blogs/how-does-k-nearest-neighbor-works-machine-learning-classification-problem
import pandas as pd
# import the data from iris.csv
iris_df = pd.read_csv('iris.csv')
# print out basic info about it
print (iris_df.isnull().sum())
print (iris_df.info())

from sklearn.preprocessing import LabelEncoder
# import label encoder
LE = LabelEncoder()
# use LE.fit_transform to get the "Class" values of the data and transform them into "normalized labels" -- https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html
iris_df['Class'] = LE.fit_transform(iris_df['Class'])
iris_df.head(5) # I think this is because there are 5 columns and it is setting that
# setting X and Y values
X = iris_df.drop('Class', axis = 1)
y = iris_df['Class']
# importing stuff
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

test_size = 0.30 # taking 70:30 training and test set
seed = 7  # Random numbmer seeding for reapeatability of the code
# training the data from sklearn
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
NN = KNeighborsClassifier()
# fit the data into a Neural Net?
NN.fit(X_train,y_train)
# Making y_predictions about the neural net
y_pred = NN.predict(X_test)
from sklearn.metrics import accuracy_score
metrics.confusion_matrix(y_test, y_pred)
# setting x accuracy to test accuracy
print(("Test accuracy: ", NN.score(X_test, y_test)))
print(("Train accuracy: ",NN.score(X_train, y_train)))

import numpy as np
from sklearn.model_selection import cross_val_score
print(X_train.shape[0])
print (int(np.sqrt(X_train.shape[0])))
maxK = int(np.sqrt(X_train.shape[0]))
print(maxK)



