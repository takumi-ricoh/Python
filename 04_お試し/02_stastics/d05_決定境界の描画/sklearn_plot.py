# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:49:03 2016

@author: p000495138
"""
import sklearn.datasets
import sklearn.linear_model
import sklearn.tree
import sklearn.ensemble
import sklearn.neighbors
import sklearn.naive_bayes
import sklearn
import numpy as np
import matplotlib.pyplot as plt


###########決定境界############
# Helper function to plot a decision boundary.
# If you don't fully understand this function don't worry, it just generates the contour plot below.
def plot_decision_boundary(pred_func):
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral)


# データを生成してプロットする
np.random.seed(0)
X, y = sklearn.datasets.make_moons(200, noise=0.20)
plt.scatter(X[:,0], X[:,1], s=40, c=y, cmap=plt.cm.Spectral)

################アルゴリズム###################
# ロジスティック回帰モデルを学習させる
clf1 = sklearn.linear_model.LogisticRegressionCV()
clf1.fit(X, y)
# 決定木モデル
clf2 = sklearn.tree.DecisionTreeClassifier()
clf2.fit(X, y)
# ＳＶＭ
clf3 = sklearn.svm.SVC(C=1,kernel='rbf')
clf3.fit(X, y)
# Adaboost
clf4 = sklearn.ensemble.AdaBoostClassifier()
clf4.fit(X, y)
# RandomForest
clf5 = sklearn.ensemble.RandomForestClassifier()
clf5.fit(X, y)
# KNN
clf6 = sklearn.neighbors.KNeighborsClassifier()
clf6.fit(X, y)
# ナイーブベイズ
clf7 = sklearn.naive_bayes.GaussianNB()    
clf7.fit(X, y)

# 決定境界をプロットする
fig=plt.figure(1)
plt.subplot(331)
plot_decision_boundary(lambda x: clf1.predict(x))
plt.title("Logistic Regression")
plt.subplot(332)
plot_decision_boundary(lambda x: clf2.predict(x))
plt.title("DecisionTree")
plt.subplot(333)
plot_decision_boundary(lambda x: clf3.predict(x))
plt.title("SVM")
plt.subplot(334)
plot_decision_boundary(lambda x: clf4.predict(x))
plt.title("AdaBoost")
plt.subplot(335)
plot_decision_boundary(lambda x: clf5.predict(x))
plt.title("RandomForest")
plt.subplot(336)
plot_decision_boundary(lambda x: clf6.predict(x))
plt.title("Knn")
plt.subplot(337)
plot_decision_boundary(lambda x: clf7.predict(x))
plt.title("NaiveBayes")
fig.tight_layout()