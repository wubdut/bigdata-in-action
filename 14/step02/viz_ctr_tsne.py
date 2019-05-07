# -*- coding:utf-8 -*-  
  
from time import time  
import numpy as np  
import matplotlib.pyplot as plt  
from sklearn import (manifold, datasets, decomposition)  
import os  
  
def load(dir, name_file):  
    X = []  
    Y = []  
    path = os.path.join(dir, name_file)  
    file_data = open(path, 'r')  
    for line in file_data:  
        x = []  
        for xi in line.strip().split(',')[:-2]:  
            x.append(int(xi))  
        x.append(1.0)  
        X.append(x)  
        Y.append(int(line.strip().split(',')[-1]))  
    return np.array(X), np.array(Y)  
  
  
## Function to Scale and visualize the embedding vectors  
def plot_embedding(X, y, title=None):  
    x_min, x_max = np.min(X, 0), np.max(X, 0)  
    X = (X - x_min) / (x_max - x_min)  
    plt.figure()  
    for i in range(X.shape[0]):  
        plt.text(X[i, 0], X[i, 1], str(y[i]),  
                 color=plt.cm.Set1(int(y[i]*10)),  
                 fontdict={'weight': 'bold', 'size': 9})  
    plt.xticks([]), plt.yticks([])  
    if title is not None:  
        plt.title(title)  
  
if __name__ == '__main__':  
    X, y = load('', 'data')  
    print(X[1], y[1])  
    n_samples, n_features = X.shape  
    n_neighbors = 30  
    ## Computing PCA  
    print("Computing PCA projection")  
    t0 = time()  
    X_pca = decomposition.TruncatedSVD(n_components=2).fit_transform(X)  
    plot_embedding(X_pca, y,  
                   "Principal Components projection of the digits (time %.2fs)" %  
                   (time() - t0))  
    ## Computing t-SNE  
    print("Computing t-SNE embedding")  
    tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)  
    t0 = time()  
    X_tsne = tsne.fit_transform(X)  
    plot_embedding(X_tsne, y,  
                   "t-SNE embedding of the digits (time %.2fs)" %  
                   (time() - t0))  
    plt.show()  
