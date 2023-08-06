import pandas as pd
from catboost import CatBoostRegressor
from lightgbm import LGBMRegressor
from sklearn.ensemble import (ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor)
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeRegressor
from xgboost.sklearn import XGBRegressor


# def get_dict_regress_models(seed=42):
#     '''returns a dictionary of models to be used in the training process'''

#     return {
#         'CATBOOST': CatBoostRegressor(verbose=False, random_state=seed),
#         'ELAST': ElasticNet(random_state=seed),
#         'GRADB': GradientBoostingRegressor(random_state=seed),
#         'RFR': RandomForestRegressor(verbose=1, random_state=seed),
#         'DTR': DecisionTreeRegressor(random_state=seed),
#         'XTR': ExtraTreesRegressor(random_state=seed),
#         'LGBM': LGBMRegressor(random_state=seed),
#         'XGB': XGBRegressor(use_label_encoder=False, eval_metric='error', random_state=seed),
#     }


# def create_model(reg_name, **kwargs):
#     '''returns an instantiated model to be used in the training process'''
#     try:
#         reg = get_dict_regress_models()[reg_name]
#         reg.set_params(**kwargs)
#         return reg
#     except Exception as e:
#         logger.error(f"> Error create_model({reg_name}): {e}")
#     return None


# def train_the_model(reg, x, y, use_ravel=True):
#     '''Train the model using the X and Y values. If use_ravel is True, the Y values will be raveled'''
#     try:
#         reg.fit(x, y.ravel() if use_ravel else y)
#         return reg
#     except Exception as e:
#         logger.error(f"> Error train_the_model({reg}): {e}")
#     return None


# def just_predict_model(pipe, x, scaler_y=None):
#     '''Predict X values using the model. If scaler_y is not None, it will be used to inverse transform the predicted values'''
#     predicted = pipe.predict(x)
#     if scaler_y is not None:
#         predicted = scaler_y.inverse_transform(predicted.reshape(-1, 1))
#     return predicted


# def predict_model(pipe, x_train, x_test, scaler_y=None):
#     '''Predict train and test dataset using the model. If scaler_y is not None, it will be used to inverse transform the predicted values'''
#     predicted = pipe.predict(x_train)
#     predicted_t = pipe.predict(x_test)
#     if scaler_y is not None:
#         predicted = scaler_y.inverse_transform(predicted.reshape(-1, 1))
#         predicted_t = scaler_y.inverse_transform(predicted_t.reshape(-1, 1))
#     return predicted, predicted_t


# def calc_mape_mae(truth, pred):
#     '''Calculate MAPE and MAE from truth and pred values'''
#     df = pd.DataFrame({'truth': truth.ravel(), 'pred': pred.ravel()})
#     # Replace negative predictions with 0
#     df['pred'] = df['pred'].clip(lower=0)
#     df['error'] = abs(df['pred'] - df['truth'])
#     mape = df['error'].sum() / df['truth'].sum()
#     mae = df['error'].mean()
#     return mape, mae, df
