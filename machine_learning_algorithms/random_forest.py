import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import matplotlib.pyplot as plt


def RF(features_df, n):
    X = features_df.iloc[:, :n]
    y = features_df.iloc[:, n]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=10)

    sc = StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    classifier = RandomForestClassifier(n_estimators=2000, criterion='entropy')
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    #print(confusion_matrix(y_test, y_pred))
    #print(classification_report(y_test, y_pred))
    #print(accuracy_score(y_test, y_pred))
    #np.set_printoptions(precision=2)
    #plot_confusion_matrix(y_test, y_pred, normalize=True, title='Normalized confusion matrix')
    #plt.show()
    return accuracy_score(y_test, y_pred)



def plot_confusion_matrix(y_true, y_pred, normalize=False, title=None, cmap=plt.cm.Blues):
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    cm = confusion_matrix(y_true, y_pred)
    # classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # xticklabels=classes, yticklabels=classes, title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # plt.step(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt), ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax
