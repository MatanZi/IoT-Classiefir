from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#packdata = pd.read_csv("features.csv")

#packdata.shape

#3packdata.head()

#X = packdata.drop('Class', axis=1)
#y = packdata['Class']

def SVM(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

    clf = SVC(gamma='scale', decision_function_shape='ovo')
    clf.fit(X,y)
    SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape='ovo',degree=3,gamma='scale', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    dec = clf.decision_function([[1]])
    print(dec.shape[1])

    #svm_predictions = svm_model_linear.predict(X_test)

    #accuracy = svm_model_linear.score(X_test, y_test)

    #cm = confusion_matrix(y_test, svm_predictions)
    #print(confusion_matrix(y_test, y_pred))
    #print(classification_report(y_test,y_pred))