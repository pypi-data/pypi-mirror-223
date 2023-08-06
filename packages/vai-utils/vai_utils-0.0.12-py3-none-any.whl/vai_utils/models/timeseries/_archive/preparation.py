
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
# from func.helpers import DEP
# from func.preprocess import check_ds_config


# def train_test_sp(df):
#     # Split the dataset into train and test
#     pos_to_split = int(len(df) * 0.8)
#     df = df.reset_index(drop=False)
#     df_train = df[df.index < pos_to_split].set_index('cd')
#     df_test = df[df.index >= pos_to_split].set_index('cd')

#     # Split the dataset into x_train x_test, and y_train y_test
#     x_train = df_train.drop(columns=[DEP]).copy()
#     y_train = df_train[DEP].copy()
#     x_test = df_test.drop(columns=[DEP]).copy()
#     y_test = df_test[DEP].copy()
#     return x_train, x_test, y_train, y_test


# def scale_and_pca_df(x, y, scaler_x=None, scaler_y=None, scaler_pca=None, conf=None):
#     '''Scale and PCA the dataset. 
#     If scaler_x, scaler_y or scaler_pca are  None: We do fit_transform
#     If scaler_x, scaler_y or scaler_pca are not None: We just do transform
#     Returns x and y (scaled and reduced), scaler_x, scaler_y, scaler_pca
#     '''
#     conf = check_ds_config(conf)
#     y = y.to_numpy().reshape(-1, 1)
#     # Scaling the dataset
#     if conf['do_scale']:
#         if scaler_x is None:
#             scaler_x = StandardScaler(
#             ) if conf['scaler_x'] == 'std' else MinMaxScaler()
#             x = scaler_x.fit_transform(x)
#         else:
#             x = scaler_x.transform(x)

#     if conf['scale_y']:
#         if scaler_y is None:
#             scaler_y = StandardScaler(
#             ) if conf['scaler_y'] == 'std' else MinMaxScaler()
#             y = scaler_y.fit_transform(y)
#         else:
#             y = scaler_y.transform(y)

#     if conf['do_pca']:
#         if scaler_pca is None:
#             scaler_pca = PCA(n_components=.995)
#             x = scaler_pca.fit_transform(x)
#         else:
#             x = scaler_pca.transform(x)

#     return x, y, scaler_x, scaler_y, scaler_pca
