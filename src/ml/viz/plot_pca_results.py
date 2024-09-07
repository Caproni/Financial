#!/usr/local/bin/python
"""
Author: Edmund Bennett
Copyright 2024
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import plotly.express as px

from ..utils import log


def plot_pca_results(model_input_data: pd.DataFrame):
    """Plots the explained variance (standard deviation) calculated according to PCA.

    Args:
        model_input_data (pd.DataFrame): Model input data.
    """
    log.function_call()

    feature_names = model_input_data.columns

    scaler = StandardScaler()
    model_input_data_scaled = scaler.fit_transform(model_input_data)

    pca = PCA(n_components=len(feature_names))
    model_input_data_scaled_pca = pca.fit_transform(model_input_data_scaled)

    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    pca_loading_df = pd.DataFrame(
        loadings,
        index=feature_names,
        columns=[f"PC{i+1}" for i in range(pca.n_components_)],
    )

    fig = px.bar(
        pca_loading_df["PC1"].sort_values(ascending=True),
        orientation="h",
        labels={"value": "Feature Loadings", "index": "Features"},
        title="Feature Contribution to PC1",
    )

    fig.show()
