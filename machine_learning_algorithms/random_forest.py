from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from __main__ import Sample
import numpy as np
import pandas as pd
import numpy as np

def RF(X, y, definitions):


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=21)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    classifier = RandomForestClassifier(n_estimators=20, criterion='entropy', random_state=42)
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))
    # Reverse factorize (converting y_pred from 0s,1s and 2s to Iris-setosa, Iris-versicolor and Iris-virginica
    reversefactor = dict(zip(range(4), definitions))
  #  y_test = np.vectorize(reversefactor.get)(y_test)
  #  y_pred = np.vectorize(reversefactor.get)(y_pred)

    #print(pd.crosstab(y_test, y_pred, rownames=['Actual Species'], colnames=['Predicted Species']))

#    classifier = RandomForestClassifier(n_estimators=20, random_state=0)
#    classifier.fit(X_train, y_train)
#    y_pred = classifier.predict(X_test)

    #print(confusion_matrix(y_test, y_pred))
    #print(classification_report(y_test, y_pred))
    #print(accuracy_score(y_test, y_pred))
