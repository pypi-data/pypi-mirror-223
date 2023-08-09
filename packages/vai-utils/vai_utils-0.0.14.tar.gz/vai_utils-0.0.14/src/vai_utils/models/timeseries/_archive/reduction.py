import numpy as np
import pandas as pd

def cap_outliers(s):
    if isinstance(s, pd.Series):
        s_ = s.copy()
        s_ = s_.dropna().tolist()
        s2 = pd.Series(index=s.index)
    else:
        s_ = s
        s2 = []

    Q1 = np.percentile(s_, 25)
    Q3 = np.percentile(s_, 75)
    IQR = Q3 - Q1
    upper = Q3 + 1.5 * IQR
    lower = Q1 - 1.5 * IQR

    for i, x in enumerate(s):
        if pd.notnull(x):
            if x > upper:
                s2[i] = upper
            elif x < lower:
                s2[i] = lower
            else:
                s2[i] = x
        else:
            s2[i] = np.nan

    return s2


def remove_redundant_features(df, target, threshold=0.9, drop=True):
    """Removes redundant features based on the Pearson correlation coefficient.
    Args:
        df (pandas.DataFrame): The dataset containing the features.
        target (str): The name of the target column.
        threshold (float, optional): The threshold above which the correlation coefficient is considered redundant. Defaults to 0.9.
        drop (bool, optional): Whether to drop the redundant features or not. Defaults to True.
    Returns:
        df (pandas.DataFrame): The dataset with the redundant features dropped.
        cols_to_drop (list): The columns that were dropped.
    """

    # Check if the target column is in the dataframe
    if target not in df.columns:
        raise KeyError(
            f'The target column "{target}" does not exist in the dataframe.')

    # Copy the target column
    dependent_series = df[target].copy()

    # Sample the dataframe to reduce the time to calculate the correlation matrix
    dfs = df.copy().sample(min([10_000, len(df)]), random_state=42)

    # Calculate the Pearson correlation matrix and Convert the matrix to a dictionary
    corr_matrix = dfs.corr(method='pearson').abs()
    corr_dict = corr_matrix[[target]].reset_index(
        drop=False).to_dict('records')
    corr_dict = {k['index']: k[target] for k in corr_dict}

    # Create a list to store the columns to drop
    cols_to_drop = []
    dict_cols_to_drop = []
    for i, c in enumerate(corr_matrix.columns):
        for y, f in enumerate(corr_matrix[c].index):
            # Skip the diagonal and lower triangle elements
            if y >= i:
                continue
            # Check if the correlation coefficient is above the threshold and append the column with the lowest corr coef to the list
            if corr_matrix[c].loc[f] > threshold:
                dict_cols_to_drop.append(
                    {"f0": c, "f1": f, "corr_f0f1": corr_matrix[c].loc[f], "f0_corr": corr_dict[c], "f1_corr": corr_dict[f], "remove": c if corr_dict[c] < corr_dict[f] else f})
                cols_to_drop.append(c if corr_dict[c] < corr_dict[f] else f)

    # Remove duplicate columns and the target column
    cols_to_drop = [d for d in list(set(cols_to_drop)) if d != target]

    if drop:
        df = df.drop(cols_to_drop, axis=1)
        df[target] = dependent_series

    return df, cols_to_drop, dict_cols_to_drop


def generalized_fisher_score(dataset, target_column):
    """Calculate the Generalized Fisher Score for each feature in the dataset."""
    feature_columns = [col for col in dataset.columns if col != target_column]

    # Calculate mean and standard deviation for each feature and target
    means = dataset.mean()
    stds = dataset.std()

    gfs_scores = {}

    for feature in feature_columns:
        # Calculate the covariance matrix
        cov_matrix = np.cov(dataset[[feature, target_column]].T)

        # Calculate the Fisher score
        fisher_score = (cov_matrix[0, 1] ** 2) / \
            (stds[feature] * stds[target_column])

        # Calculate the Generalized Fisher Score
        gfs_score = (means[feature] * means[target_column] *
                     fisher_score) / (stds[feature] * stds[target_column])

        # Store the GFS score
        gfs_scores[feature] = gfs_score

    # GFS dict to DataFrame sorted by GFS score in descending order
    gfs_scores = pd.DataFrame.from_dict(gfs_scores, orient='index', columns=[
                                        'GFS'])
    gfs_scores['GFS'] = gfs_scores['GFS'].apply(lambda x: round(x, 4))
    gfs_scores = gfs_scores.sort_values(
        by='GFS', ascending=False)
    return gfs_scores
