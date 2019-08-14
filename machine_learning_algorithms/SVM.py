from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

packdata = pd.read_csv("features.csv")

packdata.shape

packdata.head()

X = packdata.drop('Class', axis=1)
y = packdata['Class']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)


svclassifier = SVC(kernel='linear')
svclassifier.fit(X_train, y_train)

y_pred = svclassifier.predict(X_test)


print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test,y_pred))