#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

from sklearn.decomposition import PCA

from src.utils import log


def run_pca(X, n_components):
    """
    Apply PCA to the input features X and return the transformed features.

    Parameters:
    X (array-like or DataFrame): The input features.
    n_components (int or float): Number of principal components to retain.
    If float, it represents the percentage of variance to retain.
    If int, it represents the number of components to keep.

    Returns:
    X_pca (array-like): The transformed features after applying PCA.
    pca (PCA object): The fitted PCA object, useful for inverse transformation or further analysis.
    """
    log.function_call()

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X)

    return X_pca, pca
