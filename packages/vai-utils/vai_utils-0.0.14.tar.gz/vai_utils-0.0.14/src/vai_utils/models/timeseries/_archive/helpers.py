# Dependent Variable (Target)

BASE_DB_DICT_CONF = {
    'remove_hours': True,
    'forward_hours': 0,
    "delta": list(range(1, 8)),
    "lag": list(range(1, 8)),
    "add_nld": True,
    "dropna": True,
    "forward": 1,
    "do_scale": True,
    "do_pca": True,
    "scale_y": True,
    "reduce": True,
    "scaler_x": "std",
    "scaler_y": "std",
    "resample": "H",
    "add_meanstd": True,
}


# def ptabulate(df):
#     # print(tabulate(df, headers='keys', tablefmt='github'))
#     print()


# def print_as_title(text):
#     print()
#     print(text)
#     print('='*len(text))
