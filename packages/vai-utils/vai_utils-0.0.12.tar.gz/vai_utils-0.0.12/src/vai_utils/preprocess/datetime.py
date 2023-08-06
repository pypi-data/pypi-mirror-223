import pandas as pd, numpy as np, datetime
from dateutil import relativedelta
from sklearn.preprocessing import MinMaxScaler


pd.options.mode.chained_assignment = None
from vai_utils import data


DEP = "count_tx7zf4t"  # count parameter for statistical methods


def main(dataset, d_params):
    '''
    Preprocess the dataset
    '''

    # Assume count is the feature if none specified
    if not d_params["x"]:  # TODO support add features for reg input too.
        dataset[DEP] = 1  # count instances
        dataset = add_counts(dataset, d_params)

        # Adding Features to the dataset TODO check
        dataset = add_features(dataset, d_params).copy()
        
        # TODO find d_types for validating them
        x_columns = dataset.columns.drop(DEP)
        d_params["x"] = {k: {"type": "NUMBER"} for k in x_columns}
        d_params["y"] = {DEP: {"type": "NUMBER"}}

        x, y, data_mappings = data.validate(d_params, dataset)  # Bin Data and Format NN Input
        dataset = pd.concat([x, y], axis=1)
    else:
        raise Exception("Error: Currently only support 'timeseries' with 'datetime'")
    
    # Reshape 2d to 3d timeseries
    x_seq, y_seq = split_x_y_sequences_in_out(
        np.concatenate((x, y), axis=1),
        n_steps_in=d_params["timeseries"]["datetime"]["steps_in"], n_steps_out=d_params["timeseries"]["datetime"]["steps_out"]
    )

    return x_seq.copy(), y_seq.copy(), data_mappings



def add_counts(dataset, d_params):
    """Add Statistics, but only works for "x" not definted"""

    if any(t in d_params["timeseries"]["datetime"]["step"] for t in ["hour", "day", "T"]):

        # Resample the dataframe by hour and sum the count_tx7zf4t values
        dataset = dataset.sort_values(by='datetime')

        # TODO add preiod (e.g. 3T) between start and time
        if 'hour' in d_params["timeseries"]["datetime"]['step']:
            return dataset.resample('H').sum().copy()
        elif 'day' in d_params["timeseries"]["datetime"]['step']:
            return dataset.resample('D').sum().copy()
        # TODO support T
        # elif 'T' in d_params["timeseries"]["datetime"]['step']:
        # return dataset.resample(d_params["timeseries"]["datetime"]['step']).sum().copy()
        else:
            raise Exception(f"Error: 'datetime' only compatible with 'step'")
    else:
        raise Exception(f"Error: Currently only support datetime sorting")


def add_features(df, d_params):
    '''Add features to the dataframe
    - dow: day of week
    - doy: day of year
    - hour: hour of day
    - month: month of year
    - nld: non labour day
    - ct_lag_{i}: lagged value of ct
    - ct_delta_{i}: delta of ct
    '''
    df['dow'] = df.index.dayofweek
    df['hour'] = df.index.hour
    df['doy'] = df.index.dayofyear
    df['month'] = df.index.month
    df['day'] = df.index.day

    # Hours that the bussiness is not working TODO update this
    if "time-window" in d_params['timeseries']:
        start_time, end_time = d_params["timeseries"]["time-window"]
        df = df.between_time(start_time, end_time)

    # Calc Lag and Delta
    for i in range(1, d_params["timeseries"]["datetime"]['lag']):
        df.loc[:, f'ct_lag_{i}'] = df[DEP].shift(i)

    for i in range(1, d_params["timeseries"]["datetime"]['delta']):
        df.loc[:, f'ct_delta_{i}'] = df[DEP].diff(i)

    # Non Labour Days
    if d_params["timeseries"]["datetime"]['add_nld']:
        df = add_non_labour_days(df)

    # MeanStd hour
    if d_params["timeseries"]["datetime"]['add_meanstd']:
        df = add_mean_std(df, 'hour', DEP)
        df = add_mean_std(df, 'dow', DEP)
        df = add_mean_std(df, 'day', DEP)

    # Sort the columns
    df = df[sorted(df.columns)]
    
    return df.dropna()


def fix_na(df):
    for c in df.columns:
        if df[c].dtype != 'object':
            df[c] = df[c].replace([np.inf, -np.inf], np.NaN)
            df[c] = df[c].interpolate(method='linear', limit_direction='both')
    return df


def add_non_labour_days(df):
    '''Add a column with 1 if the day is a non labour day and 0 otherwise'''
    nld = get_non_labour_days()
    dfx = df.copy()
    dfx['month-day'] = [(m, d) for m, d in zip(df.index.month, df.index.day)]
    df['nld'] = (dfx['month-day'].apply(lambda x: x in nld)).astype(int)
    return df


def get_non_labour_days():
    '''Harcoded for 2022'''
    return [
        (1, 1), (1, 17), (2, 21),
        (5, 30), (7, 4), (9, 5),
        (10, 10), (11, 11), (11, 24),
        (12, 26)
    ]


def day_init_end_daylight_adj(year=2022):
    # Get the date for the start of daylight saving time
    start_date = datetime.datetime(year, 3, 1)  # Start from the 1st of March

    # Find the second Sunday in March
    while start_date.weekday() != 6:  # Check if the current day is not Sunday
        # Move to the next day
        start_date += relativedelta.relativedelta(days=1)

    # Get the date for the end of daylight saving time
    end_date = datetime.datetime(year, 11, 1)  # Start from the 1st of November

    # Find the first Sunday in November
    while end_date.weekday() != 6:  # Check if the current day is not Sunday
        end_date += relativedelta.relativedelta(days=1)  # Move to the next day

    # Get the day of the year when daylight saving time ends
    return start_date, end_date


def adjust_daylight_saving_time(df):
    start_date, end_date = day_init_end_daylight_adj()
    df['dst'] = (
        df.index >= start_date) & (df.index <= end_date)
    # df[df['daylight_saving_time']].index = df[df['daylight_saving_time']#].index - relativedelta.relativedelta(hours=1)
    df['dst'] = df['dst'].astype(int)
    return df


def add_mean_std(df, field, dep):
    df = df.copy().reset_index(drop=False)
    df0 = pd.DataFrame(df.groupby(field)[dep].mean()).reset_index(
        drop=False).rename(columns={dep: f'{field}_mean'})
    df1 = pd.DataFrame(df.groupby(field)[DEP].std()).reset_index(
        drop=False).rename(columns={dep: f'{field}_std'})
    dfx = pd.merge(df, df0, on=field, how='left')
    dfx = pd.merge(dfx, df1, on=field, how='left')
    dfx = dfx.set_index('datetime', drop=True)
    return dfx


def split_x_y_sequences_in_out(sequences, n_steps_in: int = 3, n_steps_out: int = 1):
    """Split a multivariate sequence into X,y samples

    Args: 
        sequences (numpy array)
        n_steps_in (int): number of input time steps
        n_steps_out (int): number of output time steps

    Returns:
        X (numpy array): input sequences
        y (numpy array): output sequences
    """
    X = [sequences[i:i+n_steps_in, :-1]
         for i in range(len(sequences)-n_steps_in-n_steps_out+1)]
    y = [sequences[i+n_steps_in:i+n_steps_in+n_steps_out, -1]
         for i in range(len(sequences)-n_steps_in-n_steps_out+1)]
    return np.array(X, dtype=float), np.array(y, dtype=float)

