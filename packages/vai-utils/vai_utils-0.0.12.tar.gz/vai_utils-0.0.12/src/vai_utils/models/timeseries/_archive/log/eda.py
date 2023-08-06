
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

# from func.helpers import ptabulate


# def get_columns_of_dtype(df, dty=None, data=False):
#     """get columns of dtype included in dty list"""
#     dty_dict = {
#         'obj': ['object'],
#         'num': ['float', 'int', 'int64', 'float64', 'int32', 'float32', 'int16', 'float16', 'int8'],
#         'bool': ['bool'],
#         'cat': ['category'],
#         'date': ['datetime64']
#     }

#     if not dty:  # if no type is specified, default to object type
#         dty = ["obj"]
#     # convert single string to list if necessary
#     if isinstance(dty, str):
#         dty = [dty]

#     # create a list of all the types specified in the argument
#     dty_list = []
#     _ = [dty_list.extend(dty_dict[t]) for t in dty if t in dty_dict]

#     return df.copy().select_dtypes(include=dty_list) if data else list(df.select_dtypes(include=dty_list).columns)


# def correlate_a_single_df_column(df, column):
#     """Correlate a single column with all other columns
#     Args:
#         df (pd.DataFrame): dataframe to correlate
#         column (str): column to correlate
#     Returns:
#         pd.DataFrame: correlation table
#     """

#     df = df.copy()
#     if len(df) > 20000:
#         df = df.sample(n=20000, random_state=42)
#     if isinstance(column, list):
#         column = column[0]
#     num_cols = get_columns_of_dtype(df, dty='num')
#     dfc = pd.DataFrame(df[num_cols].corrwith(
#         df[column], method='pearson')).reset_index(drop=False)
#     dfc.columns = ['feature', 'corr']
#     dfc['corr_abs'] = dfc['corr'].abs()
#     dfc = dfc.sort_values(
#         'corr_abs', ascending=False).iloc[1:].dropna().reset_index(drop=True)
#     return dfc


# def plot_all_histograms_from_a_df(df, title=None):
#     """plots all histograms from a dataframe df in a single figure
#     Seaborn is too slow for this task
#     """
#     if title is None:
#         title = 'Histograms of Features'
#     cols = 5
#     rows = len(df.columns)//cols + 1
#     fig = plt.figure(figsize=(cols*4, rows*2))

#     # for each column, plot a histogram
#     for i, col in enumerate(df.columns):
#         _ = fig.add_subplot(rows, cols, i+1)
#         plt.hist(x=df[col], bins=30)
#         plt.title(col)

#     fig.suptitle(title, fontsize=20, y=1.005)
#     fig.tight_layout()
#     plt.show()


# def plot_all_boxplot_from_a_df(df, title=None):
#     """ Plot Boxplots of Features from dataframe df"""
#     if title is None:
#         title = 'Boxplots of Features'
#     _, axs = plt.subplots(1, 1, figsize=(20, 4))
#     # Boxplot
#     sns.boxplot(data=df, ax=axs)
#     plt.suptitle(title, fontsize=20, y=1.005)
#     plt.tight_layout()
#     plt.show()


# def do_correlation_matrix(df, plot=False):
#     """Correlation matrix of a dataframe"""

#     # Get columns of numeric types
#     numeric_cols = get_columns_of_dtype(df, dty=['num'])
#     # Calculate the correlation matrix only for numeric columns
#     corr = df[numeric_cols].corr(method='pearson')
#     if plot:
#         # Plot the correlation matrix using a heatmap
#         sns.set_style("darkgrid")
#         plt.figure(figsize=(15, 10))
#         sns.heatmap(corr, annot=True)
#         plt.show()
#     return corr


# def fix_na(df):
#     for c in df.columns:
#         if df[c].dtype != 'object':
#             df[c] = df[c].replace([np.inf, -np.inf], np.NaN)
#             df[c] = df[c].interpolate(method='linear', limit_direction='both')
#     return df


# def calc_feat_importance(df, target):
#     """Calculate feature importance using logistic regression
#     from a dataframe and a target variable
#     Returns a dataframe with the features and importance scores
#     """

#     df = fix_na(df)

#     # Get columns of numeric types
#     cols_to_use = get_columns_of_dtype(df, dty=['num'])

#     # Creates X and y
#     X = df[cols_to_use].copy().drop(columns=target).copy()
#     y = df[target].copy()

#     dt = DecisionTreeRegressor(max_features=1.0, random_state=123)
#     # Fit the model with X and y
#     dt.fit(X, y)
#     importances = dt.feature_importances_

#     # Create a dataframe with the features and importance scores
#     feat_importance = pd.DataFrame({
#         'feature': X.columns,
#         'importance': importances
#     })
#     feat_importance['importance'] = feat_importance['importance'].apply(
#         lambda x: round(x, 4))

#     # Sort the features by importance score
#     feat_importance = feat_importance.sort_values(
#         'importance', ascending=False).reset_index(drop=True)
#     return feat_importance


# def df_explore_missing_values(df):
#     """Explore missing values in a dataframe"""
#     features_with_nan = []
#     nan_count = df.isna().sum()
#     nan_count = nan_count[nan_count > 0]
#     if len(nan_count) > 0:
#         # Sorting by feature name
#         nan_count = nan_count.reset_index(drop=False).rename(
#             columns={'index': 'feature', 0: 'nans'}).sort_values(by='feature', ascending=True)
#         # % of missing values
#         nan_count['nan_p'] = nan_count['nans'] / len(df)
#         # Unique values
#         nan_count['unique_values'] = [len(df[c].unique())
#                                       for c in nan_count.feature]
#         # Data type
#         nan_count['dtype'] = df[nan_count.feature].dtype.str
#         # Save features with nan values for further analysis
#         features_with_nan = sorted(nan_count.feature)

#     return features_with_nan


# def vbar_plot(x, y, title, xlabel=None, ylabel=None, rotate=False, palette='Blues_r', figsize=(20, 5)):
#     sns.set_theme(style="whitegrid")
#     plt.figure(figsize=figsize)
#     sns.barplot(x=x, y=y, palette=palette)
#     if xlabel:
#         plt.xlabel(xlabel)
#     if ylabel:
#         plt.ylabel(ylabel)
#     plt.title(title)
#     # Add data labels to the bars
#     for i, value in enumerate(y):
#         plt.text(i, value, f'{value:.4f}', ha='center', va='bottom')
#     if rotate:
#         plt.xticks(rotation=45)

#     ylim_min = min(y) - 0.1 * max(y)
#     ylim_max = max(y) + 0.1 * max(y)
#     plt.ylim(ylim_min, ylim_max)

#     plt.tight_layout()
#     plt.show()


# def vbar_2_plots(df, title, xlabel=None, ylabel=None, rotate=False):
#     cols = df.columns.tolist()

#     # Set the width of each bar
#     bar_width = 0.35

#     # Calculate the positions of the bars on the x-axis
#     r1 = np.arange(len(df))
#     r2 = [x + bar_width for x in r1]

#     plt.figure(figsize=(10, 6))

#     # Plot the bars for mape_0
#     plt.bar(r1, df[cols[1]], width=bar_width, label=cols[1],
#             color='#536DFE', edgecolor='black')

#     # Plot the bars for mape_hyper
#     plt.bar(r2, df[cols[2]], width=bar_width,
#             label=cols[2], color='#3F51B5', edgecolor='black')
#     if xlabel is not None:
#         plt.xlabel(xlabel)
#     if ylabel is not None:
#         plt.ylabel(ylabel)

#     plt.title(title)

#     # Add data labels to the bars
#     for i, row in df.iterrows():
#         plt.text(i, row[cols[1]],
#                  f'{row[cols[1]]:.4f}', ha='center', va='bottom')
#         plt.text(i + bar_width, row[cols[2]],
#                  f'{row[cols[2]]:.4f}', ha='center', va='bottom')

#     # Set the x-axis tick positions and labels
#     if rotate:
#         plt.xticks([r + bar_width/2 for r in range(len(df))],
#                    df[cols[0]], rotation=45)
#     else:
#         plt.xticks([r + bar_width/2 for r in range(len(df))],
#                    df[cols[0]])

#     plt.legend()
#     plt.tight_layout()
#     plt.show()
